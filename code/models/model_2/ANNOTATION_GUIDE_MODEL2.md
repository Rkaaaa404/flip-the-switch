# Model 2 Annotation Guide: Surface Defect Classes

The visual reference for drawing and checking bounding boxes for Model 2, the surface defect detector. The class ids are Indonesian and are kept as stored ids. The English label in brackets is what the Receiving QC Room shows.

## The four classes

| Id | Class | Hotkey | Label color | In short |
|---|---|---|---|---|
| 0 | `sisik_sisa` (scale damage) | `1` | Orange | Attached parasites, parasite spots, loose or rough scales |
| 1 | `warna_abnormal` (red lesion) | `2` | Red | Red lesions, skin hemorrhage, Aeromonas patches, gill inflammation |
| 2 | `luka_robekan` (open wound) | `3` | Yellow | Ulcers, torn fins or tail (fin rot), *Saprolegnia* fungus |
| 3 | `lendir_berlebih` (excess mucus) | `4` | Purple | Thick cloudy mucus, white tail disease (WTD), excess white mucus |

These match the Label Studio template [`02_label_studio_config.xml`](02_label_studio_config.xml) one to one.

## Visual criteria

### 0. `sisik_sisa`: scale damage (orange)

- Parasites attached to the body or scales, such as *Argulus* (fish lice) or anchor worm.
- Scales partly detached, sticking out, or roughly damaged.
- Small, localized white or black spots caused by parasites.

**Includes:** parasitic diseases (PD) from Roboflow and Hugging Face; worms or lice visible on the body.
**Box:** tight around the parasite or the group of raised scales.

### 1. `warna_abnormal`: red lesion (red)

- Red rash, red spots, bleeding under the skin or scales (hemorrhage).
- Red swelling from *Aeromonas* infection.
- Abnormal gill or skin color: faded, bruised or locally dark.

**Includes:** Bacterial Red Disease (BRD), Aeromoniasis (BDA), Bacterial Gill Disease (BGD), redness on the belly or back.
**Box:** around the whole red or inflamed area.

### 2. `luka_robekan`: open wound (yellow)

- **Ulcer:** flesh torn, holed or peeled down to the inner layer.
- **Fin or tail rot:** pectoral, dorsal or tail fins ragged, torn or missing.
- **Fungus (*Saprolegnia*):** white or grey cotton-like threads growing over a wound.

**Includes:** Fungal Disease Saprolegniasis (FDS), skin ulcer, tail rot, fin rot, tears from physical impact.
**Box:** around the torn or holed tissue and any fungus threads around it.

### 3. `lendir_berlebih`: excess mucus (purple)

- A very thick, cloudy or whitish mucus layer on the body or tail.
- **White tail disease (WTD):** the tail or rear body turns pale or cloudy white from built-up mucus after a viral or bacterial infection.
- Spreading white patches that form a film, not fungal threads.

**Includes:** white tail disease (WTD), excess or abnormal mucus.
**Box:** around the cloudy or white mucus film.

## Edge cases

1. **Healthy fish:** draw **no box at all**. Leave the label empty (background).
2. **Overlapping defects:** if a wound is surrounded by redness, label it `luka_robekan` when the flesh is damaged or holed. Redness without an open wound is `warna_abnormal`.
3. **Fungus or mucus:** fungus (`luka_robekan`) is **raised, cotton-like threads** attached to a wound. Mucus (`lendir_berlebih`) is a **smooth, cloudy white film** spread evenly over the skin or tail.
