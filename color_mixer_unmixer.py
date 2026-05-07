import tkinter as tk
from tkinter import ttk


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


class ColorTool(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Color Mixer / Unmixer")
        self.geometry("760x460")
        self.resizable(False, False)

        self.mix_a_var = tk.StringVar(value="#FF0000")
        self.mix_b_var = tk.StringVar(value="#0000FF")
        self.mix_ratio_var = tk.DoubleVar(value=50.0)
        self.mix_result_var = tk.StringVar(value="#800080")

        self.unmix_mixed_var = tk.StringVar(value="#800080")
        self.unmix_known_var = tk.StringVar(value="#FF0000")
        self.unmix_ratio_var = tk.DoubleVar(value=50.0)
        self.unmix_result_var = tk.StringVar(value="#0000FF")

        self.status_var = tk.StringVar(value="Enter hex colors to mix or unmix.")

        self._build_ui()
        self._bind_live_previews()
        self.update_mix()
        self.update_unmix()

    def _build_ui(self) -> None:
        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Color.TLabel", font=("Consolas", 11, "bold"))

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

    def _bind_live_previews(self) -> None:
        self.mix_a_var.trace_add("write", lambda *_args: self._refresh_input_preview(self.mix_a_var, self.mix_a_preview))
        self.mix_b_var.trace_add("write", lambda *_args: self._refresh_input_preview(self.mix_b_var, self.mix_b_preview))
        self.unmix_mixed_var.trace_add(
            "write", lambda *_args: self._refresh_input_preview(self.unmix_mixed_var, self.unmix_mixed_preview)
        )
        self.unmix_known_var.trace_add(
            "write", lambda *_args: self._refresh_input_preview(self.unmix_known_var, self.unmix_known_preview)
        )

    def _build_mixer(self, parent: ttk.LabelFrame) -> None:
        ttk.Label(parent, text="Color A").grid(row=0, column=0, sticky="w")
        ttk.Entry(parent, textvariable=self.mix_a_var, width=12).grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.mix_a_preview = tk.Label(parent, width=12, height=2, bg="#FF0000", relief="ridge", bd=1)
        self.mix_a_preview.grid(row=0, column=2, padx=(10, 0), pady=4)

        ttk.Label(parent, text="Color B").grid(row=1, column=0, sticky="w")
        ttk.Entry(parent, textvariable=self.mix_b_var, width=12).grid(row=1, column=1, sticky="w", padx=(8, 0))
        self.mix_b_preview = tk.Label(parent, width=12, height=2, bg="#0000FF", relief="ridge", bd=1)
        self.mix_b_preview.grid(row=1, column=2, padx=(10, 0), pady=4)

        ttk.Label(parent, text="Blend Toward B").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Scale(
            parent,
            from_=0,
            to=100,
            variable=self.mix_ratio_var,
            command=lambda _value: self.update_mix(),
            length=220,
        ).grid(row=2, column=1, columnspan=2, sticky="w", padx=(8, 0), pady=(12, 0))

        self.mix_ratio_label = ttk.Label(parent, text="50%")
        self.mix_ratio_label.grid(row=3, column=1, sticky="w", padx=(8, 0))

        ttk.Button(parent, text="Mix Colors", command=self.update_mix).grid(row=4, column=0, pady=(14, 0), sticky="w")
        ttk.Entry(parent, textvariable=self.mix_result_var, width=12, state="readonly").grid(
            row=4, column=1, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        self.mix_result_preview = tk.Label(parent, width=12, height=3, bg="#800080", relief="ridge", bd=1)
        self.mix_result_preview.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))

    def _build_unmixer(self, parent: ttk.LabelFrame) -> None:
        ttk.Label(parent, text="Mixed Color").grid(row=0, column=0, sticky="w")
        ttk.Entry(parent, textvariable=self.unmix_mixed_var, width=12).grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.unmix_mixed_preview = tk.Label(parent, width=12, height=2, bg="#800080", relief="ridge", bd=1)
        self.unmix_mixed_preview.grid(row=0, column=2, padx=(10, 0), pady=4)

        ttk.Label(parent, text="Known Base").grid(row=1, column=0, sticky="w")
        ttk.Entry(parent, textvariable=self.unmix_known_var, width=12).grid(row=1, column=1, sticky="w", padx=(8, 0))
        self.unmix_known_preview = tk.Label(parent, width=12, height=2, bg="#FF0000", relief="ridge", bd=1)
        self.unmix_known_preview.grid(row=1, column=2, padx=(10, 0), pady=4)

        ttk.Label(parent, text="Known Blend %").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Scale(
            parent,
            from_=1,
            to=99,
            variable=self.unmix_ratio_var,
            command=lambda _value: self.update_unmix(),
            length=220,
        ).grid(row=2, column=1, columnspan=2, sticky="w", padx=(8, 0), pady=(12, 0))

        self.unmix_ratio_label = ttk.Label(parent, text="50%")
        self.unmix_ratio_label.grid(row=3, column=1, sticky="w", padx=(8, 0))

        ttk.Button(parent, text="Solve Missing Color", command=self.update_unmix).grid(row=4, column=0, pady=(14, 0), sticky="w")
        ttk.Entry(parent, textvariable=self.unmix_result_var, width=12, state="readonly").grid(
            row=4, column=1, sticky="w", padx=(8, 0), pady=(14, 0)
        )
        self.unmix_result_preview = tk.Label(parent, width=12, height=3, bg="#0000FF", relief="ridge", bd=1)
        self.unmix_result_preview.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))

    def _update_preview(self, widget: tk.Label, color: tuple[int, int, int]) -> None:
        widget.configure(bg=rgb_to_hex(color))

    def _refresh_input_preview(self, color_var: tk.StringVar, widget: tk.Label) -> None:
        try:
            self._update_preview(widget, parse_hex(color_var.get()))
        except ValueError:
            pass

    def update_mix(self) -> None:
        try:
            color_a = parse_hex(self.mix_a_var.get())
            color_b = parse_hex(self.mix_b_var.get())
            ratio = self.mix_ratio_var.get() / 100
            mixed = mix_colors(color_a, color_b, ratio)

            self.mix_result_var.set(rgb_to_hex(mixed))
            self.mix_ratio_label.config(text=f"{self.mix_ratio_var.get():.0f}%")
            self._update_preview(self.mix_a_preview, color_a)
            self._update_preview(self.mix_b_preview, color_b)
            self._update_preview(self.mix_result_preview, mixed)
            self.status_var.set("Mixer updated.")
        except ValueError as exc:
            self.status_var.set(str(exc))

    def update_unmix(self) -> None:
        try:
            mixed = parse_hex(self.unmix_mixed_var.get())
            known = parse_hex(self.unmix_known_var.get())
            ratio = self.unmix_ratio_var.get() / 100
            solved = unmix_color(mixed, known, ratio)

            self.unmix_result_var.set(rgb_to_hex(solved))
            self.unmix_ratio_label.config(text=f"{self.unmix_ratio_var.get():.0f}%")
            self._update_preview(self.unmix_mixed_preview, mixed)
            self._update_preview(self.unmix_known_preview, known)
            self._update_preview(self.unmix_result_preview, solved)
            self.status_var.set("Unmixer solved the missing color.")
        except ValueError as exc:
            self.status_var.set(str(exc))


if __name__ == "__main__":
    app = ColorTool()
    app.mainloop()
