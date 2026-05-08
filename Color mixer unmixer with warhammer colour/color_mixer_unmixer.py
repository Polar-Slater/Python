import tkinter as tk
from tkinter import ttk

from citadel_paints import PAINTS


CITADEL_OPTIONS = ["Custom Hex"] + sorted(PAINTS)


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


def mix_colors(color_a: tuple[int, int, int], color_b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(
        clamp_channel((1 - ratio) * channel_a + ratio * channel_b)
        for channel_a, channel_b in zip(color_a, color_b)
    )


def unmix_color(
    mixed: tuple[int, int, int],
    known: tuple[int, int, int],
    ratio: float,
) -> tuple[int, int, int]:
    if ratio <= 0:
        raise ValueError("Ratio must be greater than 0% to solve for the second color.")
    if ratio >= 1:
        raise ValueError("Ratio must be less than 100% to solve for the second color.")

    solved = []
    for mixed_channel, known_channel in zip(mixed, known):
        channel = (mixed_channel - (1 - ratio) * known_channel) / ratio
        solved.append(clamp_channel(channel))
    return tuple(solved)


class ColorInput:
    def __init__(self, parent: ttk.LabelFrame, row: int, label: str, default_hex: str, default_paint: str = "Custom Hex") -> None:
        self.paint_var = tk.StringVar(value=default_paint)
        self.hex_var = tk.StringVar(value=default_hex)

        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w")

        self.paint_combo = ttk.Combobox(
            parent,
            textvariable=self.paint_var,
            values=CITADEL_OPTIONS,
            state="readonly",
            width=26,
        )
        self.paint_combo.grid(row=row, column=1, sticky="w", padx=(8, 0))

        self.hex_entry = ttk.Entry(parent, textvariable=self.hex_var, width=12)
        self.hex_entry.grid(row=row, column=2, sticky="w", padx=(8, 0))

        self.preview = tk.Label(parent, width=12, height=2, bg=default_hex, relief="ridge", bd=1)
        self.preview.grid(row=row, column=3, padx=(10, 0), pady=4)

    def bind(self, on_change) -> None:
        self.paint_combo.bind("<<ComboboxSelected>>", lambda _event: on_change("paint"))
        self.hex_var.trace_add("write", lambda *_args: on_change("hex"))

    def set_preview(self, rgb: tuple[int, int, int]) -> None:
        self.preview.configure(bg=rgb_to_hex(rgb))


class ColorTool(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Color Mixer / Unmixer")
        self.geometry("1040x500")
        self.resizable(False, False)

        self.mix_ratio_var = tk.DoubleVar(value=50.0)
        self.mix_result_var = tk.StringVar(value="#800080")

        self.unmix_ratio_var = tk.DoubleVar(value=50.0)
        self.unmix_result_var = tk.StringVar(value="#0000FF")

        self.status_var = tk.StringVar(value="Pick a Citadel paint or type a hex color in any input.")
        self._syncing_input = False

        self._build_ui()
        self._bind_live_previews()
        self.update_mix()
        self.update_unmix()

    def _build_ui(self) -> None:
        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))

        container = ttk.Frame(self, padding=16)
        container.pack(fill="both", expand=True)

        title = ttk.Label(container, text="Color Mixer / Unmixer", style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        mixer = ttk.LabelFrame(container, text="Mixer", padding=12)
        mixer.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        unmixer = ttk.LabelFrame(container, text="Unmixer", padding=12)
        unmixer.grid(row=1, column=1, sticky="nsew")

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        self._build_mixer(mixer)
        self._build_unmixer(unmixer)

        status = ttk.Label(container, textvariable=self.status_var, foreground="#444444")
        status.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    def _build_mixer(self, parent: ttk.LabelFrame) -> None:
        self.mix_a_input = ColorInput(parent, 0, "Color A", "#FF0000")
        self.mix_b_input = ColorInput(parent, 1, "Color B", "#0000FF")

        ttk.Label(parent, text="Blend Toward B").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Scale(
            parent,
            from_=0,
            to=100,
            variable=self.mix_ratio_var,
            command=lambda _value: self.update_mix(),
            length=320,
        ).grid(row=2, column=1, columnspan=3, sticky="w", padx=(8, 0), pady=(12, 0))

        self.mix_ratio_label = ttk.Label(parent, text="50%")
        self.mix_ratio_label.grid(row=3, column=1, sticky="w", padx=(8, 0))

        ttk.Button(parent, text="Mix Colors", command=self.update_mix).grid(row=4, column=0, pady=(14, 0), sticky="w")
        ttk.Entry(parent, textvariable=self.mix_result_var, width=12, state="readonly").grid(
            row=4, column=1, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        self.mix_result_preview = tk.Label(parent, width=18, height=3, bg="#800080", relief="ridge", bd=1)
        self.mix_result_preview.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(10, 0))

    def _build_unmixer(self, parent: ttk.LabelFrame) -> None:
        self.unmix_mixed_input = ColorInput(parent, 0, "Mixed Color", "#800080")
        self.unmix_known_input = ColorInput(parent, 1, "Known Base", "#FF0000")

        ttk.Label(parent, text="Known Blend %").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Scale(
            parent,
            from_=1,
            to=99,
            variable=self.unmix_ratio_var,
            command=lambda _value: self.update_unmix(),
            length=320,
        ).grid(row=2, column=1, columnspan=3, sticky="w", padx=(8, 0), pady=(12, 0))

        self.unmix_ratio_label = ttk.Label(parent, text="50%")
        self.unmix_ratio_label.grid(row=3, column=1, sticky="w", padx=(8, 0))

        ttk.Button(parent, text="Solve Missing Color", command=self.update_unmix).grid(row=4, column=0, pady=(14, 0), sticky="w")
        ttk.Entry(parent, textvariable=self.unmix_result_var, width=12, state="readonly").grid(
            row=4, column=1, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        self.unmix_result_preview = tk.Label(parent, width=18, height=3, bg="#0000FF", relief="ridge", bd=1)
        self.unmix_result_preview.grid(row=5, column=0, columnspan=4, sticky="ew", pady=(10, 0))

    def _bind_live_previews(self) -> None:
        for color_input in (
            self.mix_a_input,
            self.mix_b_input,
            self.unmix_mixed_input,
            self.unmix_known_input,
        ):
            color_input.bind(lambda source, ci=color_input: self._handle_input_change(ci, source))

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

    def _update_preview(self, widget: tk.Label, color: tuple[int, int, int]) -> None:
        widget.configure(bg=rgb_to_hex(color))

    def _refresh_input_preview(self, color_input: ColorInput) -> None:
        try:
            color_input.set_preview(self._resolve_color(color_input))
        except ValueError:
            pass

    def update_mix(self) -> None:
        try:
            color_a = self._resolve_color(self.mix_a_input)
            color_b = self._resolve_color(self.mix_b_input)
            ratio = self.mix_ratio_var.get() / 100
            mixed = mix_colors(color_a, color_b, ratio)

            self.mix_result_var.set(rgb_to_hex(mixed))
            self.mix_ratio_label.config(text=f"{self.mix_ratio_var.get():.0f}%")
            self.mix_a_input.set_preview(color_a)
            self.mix_b_input.set_preview(color_b)
            self._update_preview(self.mix_result_preview, mixed)
            self.status_var.set("Mixer updated.")
        except ValueError as exc:
            self.status_var.set(str(exc))

    def update_unmix(self) -> None:
        try:
            mixed = self._resolve_color(self.unmix_mixed_input)
            known = self._resolve_color(self.unmix_known_input)
            ratio = self.unmix_ratio_var.get() / 100
            solved = unmix_color(mixed, known, ratio)

            self.unmix_result_var.set(rgb_to_hex(solved))
            self.unmix_ratio_label.config(text=f"{self.unmix_ratio_var.get():.0f}%")
            self.unmix_mixed_input.set_preview(mixed)
            self.unmix_known_input.set_preview(known)
            self._update_preview(self.unmix_result_preview, solved)
            self.status_var.set("Unmixer solved the missing color.")
        except ValueError as exc:
            self.status_var.set(str(exc))


if __name__ == "__main__":
    app = ColorTool()
    app.mainloop()
