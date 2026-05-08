import tkinter as tk
from tkinter import ttk

from citadel_paints import PAINTS


CITADEL_OPTIONS = ["Custom Hex"] + sorted(PAINTS)
HEX_TO_PAINT_NAME = {paint.hex_code.upper(): paint.name for paint in PAINTS.values()}


def clamp_channel(value: float) -> int:
    return max(0, min(255, round(value)))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def parse_hex(value: str) -> tuple[int, int, int]:
    cleaned = value.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError("Use a 6-digit hex color like #FF8800.")
    try:
        return tuple(int(cleaned[index:index + 2], 16) for index in range(0, 6, 2))
    except ValueError as exc:
        raise ValueError("Hex colors can only use 0-9 and A-F.") from exc


def mix_three_colors(
    color_a: tuple[int, int, int],
    color_b: tuple[int, int, int],
    color_c: tuple[int, int, int],
    weight_a: float,
    weight_b: float,
    weight_c: float,
) -> tuple[int, int, int]:
    total = weight_a + weight_b + weight_c
    if total <= 0:
        raise ValueError("At least one mixer weight must be greater than 0.")

    ratios = (weight_a / total, weight_b / total, weight_c / total)
    return tuple(
        clamp_channel(channel_a * ratios[0] + channel_b * ratios[1] + channel_c * ratios[2])
        for channel_a, channel_b, channel_c in zip(color_a, color_b, color_c)
    )


def unmix_third_color(
    mixed: tuple[int, int, int],
    known_a: tuple[int, int, int],
    known_b: tuple[int, int, int],
    percent_a: float,
    percent_b: float,
) -> tuple[int, int, int]:
    ratio_a = percent_a / 100
    ratio_b = percent_b / 100
    ratio_c = 1 - ratio_a - ratio_b

    if ratio_a < 0 or ratio_b < 0:
        raise ValueError("Known percentages must be 0% or greater.")
    if ratio_c <= 0:
        raise ValueError("Known A % plus Known B % must stay below 100%.")

    solved = []
    for mixed_channel, known_a_channel, known_b_channel in zip(mixed, known_a, known_b):
        channel = (mixed_channel - ratio_a * known_a_channel - ratio_b * known_b_channel) / ratio_c
        solved.append(clamp_channel(channel))
    return tuple(solved)


class ColorInput:
    def __init__(self, parent: ttk.LabelFrame, row: int, label: str, default_hex: str) -> None:
        self.paint_var = tk.StringVar(value="Custom Hex")
        self.hex_var = tk.StringVar(value=default_hex)

        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")

        self.paint_combo = ttk.Combobox(
            parent,
            textvariable=self.paint_var,
            values=CITADEL_OPTIONS,
            state="readonly",
            width=24,
        )
        self.paint_combo.grid(row=row, column=1, sticky="w", padx=(8, 0))

        self.hex_entry = ttk.Entry(parent, textvariable=self.hex_var, width=12)
        self.hex_entry.grid(row=row, column=2, sticky="w", padx=(8, 0))

        self.preview = tk.Label(parent, width=12, height=2, bg=default_hex, relief="ridge", bd=1)
        self.preview.grid(row=row, column=4, padx=(10, 0), pady=4)

    def bind(self, on_change) -> None:
        self.paint_combo.bind("<<ComboboxSelected>>", lambda _event: on_change("paint"))
        self.hex_var.trace_add("write", lambda *_args: on_change("hex"))

    def set_preview(self, rgb: tuple[int, int, int]) -> None:
        self.preview.configure(bg=rgb_to_hex(rgb))


class MixerWeightInput:
    def __init__(self, parent: ttk.LabelFrame, row: int, label: str, default_hex: str, default_weight: float) -> None:
        self.color_input = ColorInput(parent, row, label, default_hex)
        self.weight_var = tk.DoubleVar(value=default_weight)
        self.weight_spin = ttk.Spinbox(
            parent,
            from_=0,
            to=100,
            increment=1,
            textvariable=self.weight_var,
            width=7,
        )
        self.weight_spin.grid(row=row, column=3, sticky="w", padx=(8, 0))

    def bind(self, on_color_change, on_weight_change) -> None:
        self.color_input.bind(on_color_change)
        self.weight_var.trace_add("write", lambda *_args: on_weight_change())


class ColorToolThree(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("3-Color Mixer / Unmixer")
        self.geometry("1120x620")
        self.resizable(False, False)

        self.mix_result_var = tk.StringVar(value="#555555")
        self.mix_share_var = tk.StringVar(value="A 33.3% | B 33.3% | C 33.3%")

        self.unmix_a_percent_var = tk.DoubleVar(value=35.0)
        self.unmix_b_percent_var = tk.DoubleVar(value=35.0)
        self.unmix_remaining_var = tk.StringVar(value="Missing C %: 30%")
        self.unmix_result_var = tk.StringVar(value="#0000FF")
        self.unmix_result_name_var = tk.StringVar(value="Citadel match: none")

        self.status_var = tk.StringVar(
            value="Pick Citadel paints or type hex codes. Mixer uses three weighted colors."
        )
        self._syncing_input = False

        self._build_ui()
        self._bind_live_updates()
        self.update_mix()
        self.update_unmix()

    def _build_ui(self) -> None:
        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))

        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="3-Color Mixer / Unmixer", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        mixer = ttk.LabelFrame(container, text="3-Color Mixer", padding=12)
        mixer.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        unmixer = ttk.LabelFrame(container, text="3-Color Unmixer", padding=12)
        unmixer.grid(row=1, column=1, sticky="nsew")

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        self._build_mixer(mixer)
        self._build_unmixer(unmixer)

        ttk.Label(container, textvariable=self.status_var, foreground="#444444").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0)
        )

    def _build_mixer(self, parent: ttk.LabelFrame) -> None:
        ttk.Label(parent, text="Weight").grid(row=0, column=3, sticky="w")

        self.mix_a = MixerWeightInput(parent, 1, "Color A", "#FF0000", 1)
        self.mix_b = MixerWeightInput(parent, 2, "Color B", "#00AA00", 1)
        self.mix_c = MixerWeightInput(parent, 3, "Color C", "#0000FF", 1)

        ttk.Label(parent, text="Weights are relative. They do not need to add up to 100.").grid(
            row=4, column=0, columnspan=5, sticky="w", pady=(10, 0)
        )
        ttk.Label(parent, textvariable=self.mix_share_var).grid(row=5, column=0, columnspan=5, sticky="w", pady=(6, 0))

        ttk.Button(parent, text="Mix 3 Colors", command=self.update_mix).grid(row=6, column=0, pady=(14, 0), sticky="w")
        ttk.Entry(parent, textvariable=self.mix_result_var, width=12, state="readonly").grid(
            row=6, column=1, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        self.mix_result_preview = tk.Label(parent, width=18, height=4, bg="#555555", relief="ridge", bd=1)
        self.mix_result_preview.grid(row=7, column=0, columnspan=5, sticky="ew", pady=(10, 0))

    def _build_unmixer(self, parent: ttk.LabelFrame) -> None:
        ttk.Label(parent, text="% Share").grid(row=0, column=3, sticky="w")

        self.unmix_mixed = ColorInput(parent, 1, "Mixed Color", "#6B3A55")
        self.unmix_known_a = ColorInput(parent, 2, "Known A", "#FF0000")
        self.unmix_known_b = ColorInput(parent, 3, "Known B", "#00AA00")

        self.unmix_a_percent_spin = ttk.Spinbox(
            parent,
            from_=0,
            to=99,
            increment=1,
            textvariable=self.unmix_a_percent_var,
            width=7,
        )
        self.unmix_a_percent_spin.grid(row=2, column=3, sticky="w", padx=(8, 0))

        self.unmix_b_percent_spin = ttk.Spinbox(
            parent,
            from_=0,
            to=99,
            increment=1,
            textvariable=self.unmix_b_percent_var,
            width=7,
        )
        self.unmix_b_percent_spin.grid(row=3, column=3, sticky="w", padx=(8, 0))

        ttk.Label(
            parent,
            text="Enter the percentages for the two known colors. The app solves the missing Color C.",
        ).grid(row=4, column=0, columnspan=5, sticky="w", pady=(10, 0))
        ttk.Label(parent, textvariable=self.unmix_remaining_var).grid(row=5, column=0, columnspan=5, sticky="w", pady=(6, 0))

        ttk.Button(parent, text="Solve Missing Color C", command=self.update_unmix).grid(
            row=6, column=0, pady=(14, 0), sticky="w"
        )
        ttk.Entry(parent, textvariable=self.unmix_result_var, width=12, state="readonly").grid(
            row=6, column=1, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        ttk.Label(parent, textvariable=self.unmix_result_name_var).grid(
            row=6, column=2, columnspan=2, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        self.unmix_result_preview = tk.Label(parent, width=18, height=4, bg="#0000FF", relief="ridge", bd=1)
        self.unmix_result_preview.grid(row=7, column=0, columnspan=5, sticky="ew", pady=(10, 0))

    def _bind_live_updates(self) -> None:
        for weighted_input in (self.mix_a, self.mix_b, self.mix_c):
            weighted_input.bind(
                lambda source, ci=weighted_input.color_input: self._handle_input_change(ci, source),
                self.update_mix,
            )

        for color_input in (self.unmix_mixed, self.unmix_known_a, self.unmix_known_b):
            color_input.bind(lambda source, ci=color_input: self._handle_input_change(ci, source))

        self.unmix_a_percent_var.trace_add("write", lambda *_args: self.update_unmix())
        self.unmix_b_percent_var.trace_add("write", lambda *_args: self.update_unmix())

    def _handle_input_change(self, color_input: ColorInput, source: str) -> None:
        if self._syncing_input:
            return

        self._syncing_input = True
        try:
            if source == "paint":
                selected_paint = color_input.paint_var.get()
                if selected_paint != "Custom Hex":
                    color_input.hex_var.set(PAINTS[selected_paint].hex_code)
            else:
                hex_value = color_input.hex_var.get().strip().upper()
                if hex_value and not hex_value.startswith("#"):
                    hex_value = f"#{hex_value}"
                    color_input.hex_var.set(hex_value)

                matching_paint = next(
                    (paint.name for paint in PAINTS.values() if paint.hex_code.upper() == hex_value),
                    None,
                )
                color_input.paint_var.set(matching_paint or "Custom Hex")

            self._refresh_input_preview(color_input)
        finally:
            self._syncing_input = False

        self.update_mix()
        self.update_unmix()

    def _resolve_color(self, color_input: ColorInput) -> tuple[int, int, int]:
        return parse_hex(color_input.hex_var.get())

    def _refresh_input_preview(self, color_input: ColorInput) -> None:
        try:
            color_input.set_preview(self._resolve_color(color_input))
        except ValueError:
            pass

    def update_mix(self) -> None:
        try:
            color_a = self._resolve_color(self.mix_a.color_input)
            color_b = self._resolve_color(self.mix_b.color_input)
            color_c = self._resolve_color(self.mix_c.color_input)

            weight_a = float(self.mix_a.weight_var.get())
            weight_b = float(self.mix_b.weight_var.get())
            weight_c = float(self.mix_c.weight_var.get())

            mixed = mix_three_colors(color_a, color_b, color_c, weight_a, weight_b, weight_c)
            total = weight_a + weight_b + weight_c
            shares = (
                100 * weight_a / total,
                100 * weight_b / total,
                100 * weight_c / total,
            )

            self.mix_result_var.set(rgb_to_hex(mixed))
            self.mix_share_var.set(f"A {shares[0]:.1f}% | B {shares[1]:.1f}% | C {shares[2]:.1f}%")
            self.mix_a.color_input.set_preview(color_a)
            self.mix_b.color_input.set_preview(color_b)
            self.mix_c.color_input.set_preview(color_c)
            self.mix_result_preview.configure(bg=rgb_to_hex(mixed))
            self.status_var.set("3-color mixer updated.")
        except (ValueError, tk.TclError) as exc:
            self.status_var.set(str(exc))

    def update_unmix(self) -> None:
        try:
            mixed = self._resolve_color(self.unmix_mixed)
            known_a = self._resolve_color(self.unmix_known_a)
            known_b = self._resolve_color(self.unmix_known_b)

            percent_a = float(self.unmix_a_percent_var.get())
            percent_b = float(self.unmix_b_percent_var.get())
            remaining = 100 - percent_a - percent_b

            solved = unmix_third_color(mixed, known_a, known_b, percent_a, percent_b)
            solved_hex = rgb_to_hex(solved)
            matching_paint_name = HEX_TO_PAINT_NAME.get(solved_hex.upper())

            self.unmix_remaining_var.set(f"Missing C %: {remaining:.1f}%")
            self.unmix_result_var.set(solved_hex)
            self.unmix_result_name_var.set(
                f"Citadel match: {matching_paint_name}" if matching_paint_name else "Citadel match: none"
            )
            self.unmix_mixed.set_preview(mixed)
            self.unmix_known_a.set_preview(known_a)
            self.unmix_known_b.set_preview(known_b)
            self.unmix_result_preview.configure(bg=solved_hex)
            self.status_var.set("3-color unmixer solved the missing Color C.")
        except (ValueError, tk.TclError) as exc:
            self.unmix_result_name_var.set("Citadel match: none")
            self.status_var.set(str(exc))


if __name__ == "__main__":
    app = ColorToolThree()
    app.mainloop()
