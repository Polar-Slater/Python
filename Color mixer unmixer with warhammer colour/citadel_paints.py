"""Citadel Colour Base and Layer paints.

Source: PaintHoarder Citadel Colour catalog pages fetched on 2026-05-07.
Hex values are display colors from the catalog pages.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Paint:
    name: str
    line: str
    hex_code: str

    @property
    def rgb(self) -> tuple[int, int, int]:
        value = self.hex_code.lstrip("#")
        return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


PAINTS: dict[str, Paint] = {
    'Abaddon Black': Paint(name='Abaddon Black', line='Base', hex_code='#000000'),
    'Averland Sunset': Paint(name='Averland Sunset', line='Base', hex_code='#FBB81C'),
    'Balthasar Gold': Paint(name='Balthasar Gold', line='Base', hex_code='#A77353'),
    'Barak-Nar Burgundy': Paint(name='Barak-Nar Burgundy', line='Base', hex_code='#451636'),
    'Bugman Glow': Paint(name='Bugman Glow', line='Base', hex_code='#804C43'),
    'Caledor Sky': Paint(name='Caledor Sky', line='Base', hex_code='#366699'),
    'Caliban Green': Paint(name='Caliban Green', line='Base', hex_code='#003D15'),
    'Castellan Green': Paint(name='Castellan Green', line='Base', hex_code='#264715'),
    'Catachan Fleshtone': Paint(name='Catachan Fleshtone', line='Base', hex_code='#442B25'),
    'Celestra Grey': Paint(name='Celestra Grey', line='Base', hex_code='#8BA3A3'),
    'Corax White': Paint(name='Corax White', line='Base', hex_code='#FFFFFF'),
    'Corvus Black': Paint(name='Corvus Black', line='Base', hex_code='#171314'),
    'Daemonette Hide': Paint(name='Daemonette Hide', line='Base', hex_code='#655F81'),
    'Death Guard Green': Paint(name='Death Guard Green', line='Base', hex_code='#6D774D'),
    'Death Korps Drab': Paint(name='Death Korps Drab', line='Base', hex_code='#3D4539'),
    'Deathworld Forest': Paint(name='Deathworld Forest', line='Base', hex_code='#556229'),
    'Dryad Bark': Paint(name='Dryad Bark', line='Base', hex_code='#2B2A24'),
    'Gal Vorbak Red': Paint(name='Gal Vorbak Red', line='Base', hex_code='#4B213C'),
    'Grey Knights Steel': Paint(name='Grey Knights Steel', line='Base', hex_code='#B0BDC6'),
    'Grey Seer': Paint(name='Grey Seer', line='Base', hex_code='#A2A5A7'),
    'Hobgrot Hide': Paint(name='Hobgrot Hide', line='Base', hex_code='#9C823B'),
    'Incubi Darkness': Paint(name='Incubi Darkness', line='Base', hex_code='#082E32'),
    'Ionrach Skin': Paint(name='Ionrach Skin', line='Base', hex_code='#97A384'),
    'Iron Hands Steel': Paint(name='Iron Hands Steel', line='Base', hex_code='#B2A79F'),
    'Iron Warriors': Paint(name='Iron Warriors', line='Base', hex_code='#706E6B'),
    'Jokaero Orange': Paint(name='Jokaero Orange', line='Base', hex_code='#ED3814'),
    'Kantor Blue': Paint(name='Kantor Blue', line='Base', hex_code='#02134E'),
    'Khorne Red': Paint(name='Khorne Red', line='Base', hex_code='#650001'),
    'Leadbelcher': Paint(name='Leadbelcher', line='Base', hex_code='#969696'),
    'Lupercal Green': Paint(name='Lupercal Green', line='Base', hex_code='#002C2B'),
    'Macragge Blue': Paint(name='Macragge Blue', line='Base', hex_code='#0F3D7C'),
    'Mechanicus Standard Grey': Paint(name='Mechanicus Standard Grey', line='Base', hex_code='#39484A'),
    'Mephiston Red': Paint(name='Mephiston Red', line='Base', hex_code='#960C09'),
    'Morghast Bone': Paint(name='Morghast Bone', line='Base', hex_code='#C0A973'),
    'Mournfang Brown': Paint(name='Mournfang Brown', line='Base', hex_code='#490F06'),
    'Naggaroth Night': Paint(name='Naggaroth Night', line='Base', hex_code='#3B2B50'),
    'Night Lords Blue': Paint(name='Night Lords Blue', line='Base', hex_code='#002B5C'),
    'Nocturne Green': Paint(name='Nocturne Green', line='Base', hex_code='#162A29'),
    'Orruk Flesh': Paint(name='Orruk Flesh', line='Base', hex_code='#97C17E'),
    'Phoenician Purple': Paint(name='Phoenician Purple', line='Base', hex_code='#440052'),
    'Rakarth Flesh': Paint(name='Rakarth Flesh', line='Base', hex_code='#9C998D'),
    'Ratskin Flesh': Paint(name='Ratskin Flesh', line='Base', hex_code='#A86648'),
    'Retributor Armour': Paint(name='Retributor Armour', line='Base', hex_code='#EDC169'),
    'Rhinox Hide': Paint(name='Rhinox Hide', line='Base', hex_code='#462F30'),
    'Runelord Brass': Paint(name='Runelord Brass', line='Base', hex_code='#8D806F'),
    'Screamer Pink': Paint(name='Screamer Pink', line='Base', hex_code='#7A0E44'),
    'Screaming Bell': Paint(name='Screaming Bell', line='Base', hex_code='#D18A5E'),
    'Steel Legion Drab': Paint(name='Steel Legion Drab', line='Base', hex_code='#584E2D'),
    'Stegadon Scale Green': Paint(name='Stegadon Scale Green', line='Base', hex_code='#06455D'),
    'The Fang': Paint(name='The Fang', line='Base', hex_code='#405B71'),
    'Thondia Brown': Paint(name='Thondia Brown', line='Base', hex_code='#4F322C'),
    'Thousand Sons Blue': Paint(name='Thousand Sons Blue', line='Base', hex_code='#00506F'),
    'Waaagh! Flesh': Paint(name='Waaagh! Flesh', line='Base', hex_code='#0B3B36'),
    'Warplock Bronze': Paint(name='Warplock Bronze', line='Base', hex_code='#B36E4F'),
    'Wraithbone': Paint(name='Wraithbone', line='Base', hex_code='#DBD1B2'),
    'XV-88': Paint(name='XV-88', line='Base', hex_code='#6C4811'),
    'Zandri Dust': Paint(name='Zandri Dust', line='Base', hex_code='#988E56'),
    'Administratum Grey': Paint(name='Administratum Grey', line='Layer', hex_code='#989C94'),
    'Ahriman Blue': Paint(name='Ahriman Blue', line='Layer', hex_code='#00708A'),
    'Alaitoc Blue': Paint(name='Alaitoc Blue', line='Layer', hex_code='#2F4F85'),
    'Altdorf Guard Blue': Paint(name='Altdorf Guard Blue', line='Layer', hex_code='#2D4696'),
    'Auric Armour Gold': Paint(name='Auric Armour Gold', line='Layer', hex_code='#FFC451'),
    'Baharroth Blue': Paint(name='Baharroth Blue', line='Layer', hex_code='#54BDCA'),
    'Balor Brown': Paint(name='Balor Brown', line='Layer', hex_code='#875408'),
    'Baneblade Brown': Paint(name='Baneblade Brown', line='Layer', hex_code='#8F7C68'),
    'Bestigor Flesh': Paint(name='Bestigor Flesh', line='Layer', hex_code='#D08951'),
    'Bloodreaver Flesh': Paint(name='Bloodreaver Flesh', line='Layer', hex_code='#6A4848'),
    'Blue Horror': Paint(name='Blue Horror', line='Layer', hex_code='#9EB5CE'),
    'Brass Scorpion': Paint(name='Brass Scorpion', line='Layer', hex_code='#A65D2C'),
    'Cadian Fleshtone': Paint(name='Cadian Fleshtone', line='Layer', hex_code='#C47652'),
    'Calgar Blue': Paint(name='Calgar Blue', line='Layer', hex_code='#2A497F'),
    'Canoptek Alloy': Paint(name='Canoptek Alloy', line='Layer', hex_code='#C3B2AC'),
    'Castellax Bronze': Paint(name='Castellax Bronze', line='Layer', hex_code='#C68351'),
    'Dark Reaper': Paint(name='Dark Reaper', line='Layer', hex_code='#354D4C'),
    'Dawnstone': Paint(name='Dawnstone', line='Layer', hex_code='#697068'),
    'Deathclaw Brown': Paint(name='Deathclaw Brown', line='Layer', hex_code='#AF634F'),
    'Dechala Lilac': Paint(name='Dechala Lilac', line='Layer', hex_code='#B598C9'),
    'Deepkin Flesh': Paint(name='Deepkin Flesh', line='Layer', hex_code='#A9B79F'),
    'Doombull Brown': Paint(name='Doombull Brown', line='Layer', hex_code='#570003'),
    'Dorn Yellow': Paint(name='Dorn Yellow', line='Layer', hex_code='#FFF55A'),
    'Elysian Green': Paint(name='Elysian Green', line='Layer', hex_code='#6B8C37'),
    'Emperor Children': Paint(name='Emperor Children', line='Layer', hex_code='#B74073'),
    'Eshin Grey': Paint(name='Eshin Grey', line='Layer', hex_code='#484B4E'),
    'Evil Sunz Scarlet': Paint(name='Evil Sunz Scarlet', line='Layer', hex_code='#C01411'),
    'Fenrisian Grey': Paint(name='Fenrisian Grey', line='Layer', hex_code='#6D94B3'),
    'Fire Dragon Bright': Paint(name='Fire Dragon Bright', line='Layer', hex_code='#F4874E'),
    'Flash Gitz Yellow': Paint(name='Flash Gitz Yellow', line='Layer', hex_code='#FFF300'),
    'Flayed One Flesh': Paint(name='Flayed One Flesh', line='Layer', hex_code='#EEC483'),
    'Fulgrim Pink': Paint(name='Fulgrim Pink', line='Layer', hex_code='#F3ABCA'),
    'Fulgurite Copper': Paint(name='Fulgurite Copper', line='Layer', hex_code='#CE8D51'),
    'Gauss Blaster Green': Paint(name='Gauss Blaster Green', line='Layer', hex_code='#7FC1A5'),
    'Gehenna Gold': Paint(name='Gehenna Gold', line='Layer', hex_code='#C96B18'),
    'Genestealer Purple': Paint(name='Genestealer Purple', line='Layer', hex_code='#7658A5'),
    'Gorthor Brown': Paint(name='Gorthor Brown', line='Layer', hex_code='#5F463F'),
    'Hashut Copper': Paint(name='Hashut Copper', line='Layer', hex_code='#BA885F'),
    'Hoeth Blue': Paint(name='Hoeth Blue', line='Layer', hex_code='#4C78AF'),
    'Ironbreaker': Paint(name='Ironbreaker', line='Layer', hex_code='#899092'),
    'Kabalite Green': Paint(name='Kabalite Green', line='Layer', hex_code='#008962'),
    'Kakophoni Purple': Paint(name='Kakophoni Purple', line='Layer', hex_code='#8869AE'),
    'Karak Stone': Paint(name='Karak Stone', line='Layer', hex_code='#B7945C'),
    'Kislev Flesh': Paint(name='Kislev Flesh', line='Layer', hex_code='#D1A570'),
    'Knight-Questor Flesh': Paint(name='Knight-Questor Flesh', line='Layer', hex_code='#996563'),
    'Krieg Khaki': Paint(name='Krieg Khaki', line='Layer', hex_code='#BCBB7E'),
    'Liberator Gold': Paint(name='Liberator Gold', line='Layer', hex_code='#E1BA7F'),
    'Loren Forest': Paint(name='Loren Forest', line='Layer', hex_code='#486C25'),
    'Lothern Blue': Paint(name='Lothern Blue', line='Layer', hex_code='#2C9BCC'),
    'Lugganath Orange': Paint(name='Lugganath Orange', line='Layer', hex_code='#F69B82'),
    'Moot Green': Paint(name='Moot Green', line='Layer', hex_code='#3DAF44'),
    'Nurgling Green': Paint(name='Nurgling Green', line='Layer', hex_code='#7E975E'),
    'Ogryn Camo': Paint(name='Ogryn Camo', line='Layer', hex_code='#96A648'),
    'Pallid Wych Flesh': Paint(name='Pallid Wych Flesh', line='Layer', hex_code='#CACCBB'),
    'Phalanx Yellow': Paint(name='Phalanx Yellow', line='Layer', hex_code='#FFE200'),
    'Pink Horror': Paint(name='Pink Horror', line='Layer', hex_code='#8E2757'),
    'Runefang Steel': Paint(name='Runefang Steel', line='Layer', hex_code='#C2C8CC'),
    'Russ Grey': Paint(name='Russ Grey', line='Layer', hex_code='#507085'),
    'Screaming Skull': Paint(name='Screaming Skull', line='Layer', hex_code='#B9C099'),
    'Skarsnik Green': Paint(name='Skarsnik Green', line='Layer', hex_code='#588F6B'),
    'Skavenblight Dinge': Paint(name='Skavenblight Dinge', line='Layer', hex_code='#45413B'),
    'Skrag Brown': Paint(name='Skrag Brown', line='Layer', hex_code='#8B4806'),
    'Skullcrusher Brass': Paint(name='Skullcrusher Brass', line='Layer', hex_code='#F4CB7A'),
    'Slaanesh Grey': Paint(name='Slaanesh Grey', line='Layer', hex_code='#8B8893'),
    'Sons of Horus Green': Paint(name='Sons of Horus Green', line='Layer', hex_code='#00545E'),
    'Sotek Green': Paint(name='Sotek Green', line='Layer', hex_code='#0B6371'),
    'Squig Orange': Paint(name='Squig Orange', line='Layer', hex_code='#A74D42'),
    'Stormhost Silver': Paint(name='Stormhost Silver', line='Layer', hex_code='#DADDDF'),
    'Stormvermin Fur': Paint(name='Stormvermin Fur', line='Layer', hex_code='#6D655F'),
    'Straken Green': Paint(name='Straken Green', line='Layer', hex_code='#597F1C'),
    'Sybarite Green': Paint(name='Sybarite Green', line='Layer', hex_code='#17A166'),
    'Sycorax Bronze': Paint(name='Sycorax Bronze', line='Layer', hex_code='#BB9F84'),
    'Tallarn Sand': Paint(name='Tallarn Sand', line='Layer', hex_code='#A07409'),
    'Tau Light Ochre': Paint(name='Tau Light Ochre', line='Layer', hex_code='#BC6B10'),
    'Teclis Blue': Paint(name='Teclis Blue', line='Layer', hex_code='#3877BF'),
    'Temple Guard Blue': Paint(name='Temple Guard Blue', line='Layer', hex_code='#239489'),
    'Thunderhawk Blue': Paint(name='Thunderhawk Blue', line='Layer', hex_code='#396A70'),
    'Troll Slayer Orange': Paint(name='Troll Slayer Orange', line='Layer', hex_code='#F16C23'),
    'Tuskgor Fur': Paint(name='Tuskgor Fur', line='Layer', hex_code='#863231'),
    'Ulthuan Grey': Paint(name='Ulthuan Grey', line='Layer', hex_code='#C4DDD5'),
    'Ungor Flesh': Paint(name='Ungor Flesh', line='Layer', hex_code='#D1A560'),
    'Ushabti Bone': Paint(name='Ushabti Bone', line='Layer', hex_code='#ABA173'),
    'Vulkan Green': Paint(name='Vulkan Green', line='Layer', hex_code='#223C2E'),
    'Warboss Green': Paint(name='Warboss Green', line='Layer', hex_code='#317E57'),
    'Warpfiend Grey': Paint(name='Warpfiend Grey', line='Layer', hex_code='#66656E'),
    'Warpstone Glow': Paint(name='Warpstone Glow', line='Layer', hex_code='#0F702A'),
    'Wazdakka Red': Paint(name='Wazdakka Red', line='Layer', hex_code='#880804'),
    'White Scar': Paint(name='White Scar', line='Layer', hex_code='#FFFFFF'),
    'Wild Rider Red': Paint(name='Wild Rider Red', line='Layer', hex_code='#E82E1B'),
    'Word Bearers Red': Paint(name='Word Bearers Red', line='Layer', hex_code='#620104'),
    'Xereus Purple': Paint(name='Xereus Purple', line='Layer', hex_code='#47125A'),
    'Yriel Yellow': Paint(name='Yriel Yellow', line='Layer', hex_code='#FFD900'),
    'Zamesi Desert': Paint(name='Zamesi Desert', line='Layer', hex_code='#D89D1B'),

}

BASE_PAINTS: dict[str, Paint] = {
    name: paint for name, paint in PAINTS.items() if paint.line == "Base"
}

LAYER_PAINTS: dict[str, Paint] = {
    name: paint for name, paint in PAINTS.items() if paint.line == "Layer"
}


def get_paint(name: str) -> Paint:
    return PAINTS[name]


if __name__ == "__main__":
    print(f"Base paints: {len(BASE_PAINTS)}")
    print(f"Layer paints: {len(LAYER_PAINTS)}")
    sample = get_paint("Mephiston Red")
    print(f"{sample.name}: {sample.hex_code} rgb={sample.rgb}")
