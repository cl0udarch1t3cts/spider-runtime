# TODO — Register restaurants

Run these commands on `spider-01`. Each request is asynchronous and creates or reuses the entry’s Doctor task.

- [ ] `Ob1139zJg0uzvHg1VlP6vA` — DaboSmoothies — Birmensdorferstrasse 285, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Ob1139zJg0uzvHg1VlP6vA",
    "businessname": "DaboSmoothies",
    "address": "Birmensdorferstrasse 285, 8003 Zürich"
  }
  JSON
  ```

- [ ] `OWjbydCNXagwj8ikDHALuw` — Piazza — Anwandstrasse 28, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OWjbydCNXagwj8ikDHALuw",
    "businessname": "Piazza",
    "address": "Idaplatz 2, 8003 Zürich"
  }
  JSON
  ```

- [ ] `AoOkoCRZ9SAeam0tWRrOgQ` — Donde Luis — Militärstrasse 114, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AoOkoCRZ9SAeam0tWRrOgQ",
    "businessname": "Donde Luis",
    "address": "Militärstrasse 114, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Jv5ZTKsgxAhxJzgfSnbFXw` — Volkshaus — Stauffacherstrasse 60, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Jv5ZTKsgxAhxJzgfSnbFXw",
    "businessname": "Volkshaus",
    "address": "Stauffacherstrasse 60, 8004 Zürich"
  }
  JSON
  ```

- [ ] `8TjEjvh9Kb6JNXnnqWYhaA` — not guilty Airgate AG — Thurgauerstrasse 40, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8TjEjvh9Kb6JNXnnqWYhaA",
    "businessname": "not guilty Airgate AG",
    "address": "Thurgauerstrasse 40, 8050 Zürich"
  }
  JSON
  ```

- [ ] `WdIsQ0-sFvwaENPvT6N03w` — Haue — Limmatquai 52, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "WdIsQ0-sFvwaENPvT6N03w",
    "businessname": "Haue",
    "address": "Limmatquai 52, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gQwfZ_z4wwJM7_5GSXwjMA` — Osteria Borgo — Niederdorfstrasse 33, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gQwfZ_z4wwJM7_5GSXwjMA",
    "businessname": "Osteria Borgo",
    "address": "Niederdorfstrasse 33, 8001 Zürich"
  }
  JSON
  ```

- [ ] `dUgMwmWlwauwgR3kL4aOug` — Centro Lusitano de Zurique zum Hüsli — Risweg 1, 8041 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dUgMwmWlwauwgR3kL4aOug",
    "businessname": "Centro Lusitano de Zurique zum Hüsli",
    "address": "Risweg 1, 8041 Zürich"
  }
  JSON
  ```

- [ ] `nDjGVaTfTILieRxg3ETaAw` — Peking Garden China-Restaurant Take Away — Langstrasse 13, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nDjGVaTfTILieRxg3ETaAw",
    "businessname": "Peking Garden China-Restaurant Take Away",
    "address": "Langstrasse 13, 8004 Zürich"
  }
  JSON
  ```

- [ ] `0N5paWNcn0yK3FmC3DP2XA` — Platzhirsch — Spitalgasse 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0N5paWNcn0yK3FmC3DP2XA",
    "businessname": "Platzhirsch",
    "address": "Spitalgasse 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Ptqf_GdJBxjcEkJ_8uStRw` — Mucho Gusto — Reitergasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Ptqf_GdJBxjcEkJ_8uStRw",
    "businessname": "Mucho Gusto",
    "address": "Reitergasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `MwSzyU-pjR5VxWMHNXDG4A` — Restaurant Tschingg am Stauffacher — Lutherstrasse 4, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "MwSzyU-pjR5VxWMHNXDG4A",
    "businessname": "Restaurant Tschingg am Stauffacher",
    "address": "Lutherstrasse 4, 8004 Zürich"
  }
  JSON
  ```

- [ ] `q2GV6lMpcKHv3u22Xuj2gw` — Restaurant Lanchid — Rebgasse 8, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "q2GV6lMpcKHv3u22Xuj2gw",
    "businessname": "Restaurant Lanchid",
    "address": "Rebgasse 8, 8004 Zürich"
  }
  JSON
  ```

- [ ] `GHVj2fGdi2vI4rtS0BCsLQ` — China Restaurant — Langstrasse 11, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GHVj2fGdi2vI4rtS0BCsLQ",
    "businessname": "China Restaurant",
    "address": "Langstrasse 11, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nMtpNpUvmIAjegc2IOjbTA` — The Studio — Dufourstrasse 23, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nMtpNpUvmIAjegc2IOjbTA",
    "businessname": "The Studio",
    "address": "Dufourstrasse 23, 8008 Zürich"
  }
  JSON
  ```

- [ ] `Zb-8lJ_Mx-BY8s6W8l30og` — Bye Bye Bar — Check-in 2, Level 2, ZRH Airport, 8058 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Zb-8lJ_Mx-BY8s6W8l30og",
    "businessname": "Bye Bye Bar",
    "address": "Check-in 2, Level 2, ZRH Airport, 8058 Zürich"
  }
  JSON
  ```

- [ ] `9zoZ_L8Y97tluPUPAQQzSQ` — Dolce Vita II — Häringstrasse 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "9zoZ_L8Y97tluPUPAQQzSQ",
    "businessname": "Dolce Vita II",
    "address": "Häringstrasse 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `rSca1EnQ1vu2YgelRgof_g` — The News Deli — 8000 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rSca1EnQ1vu2YgelRgof_g",
    "businessname": "The News Deli",
    "address": "8000 Zürich"
  }
  JSON
  ```

- [ ] `RB6zCB39qZBE8u-uVds_jQ` — Ristorante Italia — Zeughausstrasse 61, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RB6zCB39qZBE8u-uVds_jQ",
    "businessname": "Ristorante Italia",
    "address": "Zeughausstrasse 61, 8004 Zürich"
  }
  JSON
  ```

- [ ] `LxdrVU5f6eRSD_s5YbzmFw` — Cafeteria ZHAW — Lagerstrasse 45, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "LxdrVU5f6eRSD_s5YbzmFw",
    "businessname": "Cafeteria ZHAW",
    "address": "Lagerstrasse 45, 8004 Zürich"
  }
  JSON
  ```

- [ ] `O69Cn-gHItd_Jdy86vRAeA` — Monocle Shop & Cafe — Dufourstrasse 90, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "O69Cn-gHItd_Jdy86vRAeA",
    "businessname": "Monocle Shop & Cafe",
    "address": "Dufourstrasse 90, 8008 Zürich"
  }
  JSON
  ```

- [ ] `xCG0lTxFJvWtAcrutREs8w` — Swiss Chuchi Restaurant — Rosengasse 10, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xCG0lTxFJvWtAcrutREs8w",
    "businessname": "Swiss Chuchi Restaurant",
    "address": "Rosengasse 10, 8001 Zürich"
  }
  JSON
  ```

- [ ] `dwgsM2T9miPTtl8aKdxSSw` — Brasserie Café de Paris — Ankerstrasse 113, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dwgsM2T9miPTtl8aKdxSSw",
    "businessname": "Brasserie Café de Paris",
    "address": "Ankerstrasse 113, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Qr1w5U2VzDj_BGGH7UZnhA` — Restaurant Neufeld — Friesenbergstrasse 15, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Qr1w5U2VzDj_BGGH7UZnhA",
    "businessname": "Restaurant Neufeld",
    "address": "Friesenbergstrasse 15, 8055 Zürich"
  }
  JSON
  ```

- [ ] `kJFTs6JsUNLVTmUPA_gG0w` — Aggarwal AG — Kernstrasse 27, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kJFTs6JsUNLVTmUPA_gG0w",
    "businessname": "Aggarwal AG",
    "address": "Kernstrasse 27, 8004 Zürich"
  }
  JSON
  ```

- [ ] `jM6PiafIt90sLJCpwu99dA` — NENI Zürich Langstrasse — Langstrasse 150, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jM6PiafIt90sLJCpwu99dA",
    "businessname": "NENI Zürich Langstrasse",
    "address": "Langstrasse 150, 8004 Zürich"
  }
  JSON
  ```

- [ ] `1Khw8hpB1D1xydr5-OHsew` — Memolino — Leutschenbachstrasse 50, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "1Khw8hpB1D1xydr5-OHsew",
    "businessname": "Memolino",
    "address": "Leutschenbachstrasse 50, 8050 Zürich"
  }
  JSON
  ```

- [ ] `FpQBBqbeQfs1I10w2QqHbA` — Café Felix am Bellevue — Bellevueplatz 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FpQBBqbeQfs1I10w2QqHbA",
    "businessname": "Café Felix am Bellevue",
    "address": "Bellevueplatz 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `L71nxPQpJZ-KHb23Sk7Z8g` — Drinx Bar — Dufourstrasse 24, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "L71nxPQpJZ-KHb23Sk7Z8g",
    "businessname": "Drinx Bar",
    "address": "Dufourstrasse 24, 8008 Zürich"
  }
  JSON
  ```

- [ ] `AAg4H7FNsVG9NDlYaThfGg` — Rathaus-Café — Limmatquai 61, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AAg4H7FNsVG9NDlYaThfGg",
    "businessname": "Rathaus-Café",
    "address": "Limmatquai 61, 8001 Zürich"
  }
  JSON
  ```

- [ ] `8q67s0zGC1yG-i7-jLexiQ` — Neumärt — Neumarkt 28, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8q67s0zGC1yG-i7-jLexiQ",
    "businessname": "Neumärt",
    "address": "Neumarkt 28, 8001 Zürich"
  }
  JSON
  ```

- [ ] `zl8klEdtjUgXxzoUmx7m1Q` — Café Henrici — Niederdorfstrasse 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zl8klEdtjUgXxzoUmx7m1Q",
    "businessname": "Café Henrici",
    "address": "Niederdorfstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `kfNcdso5dL3HhpI9FlTiNg` — Asia Restaurant — 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kfNcdso5dL3HhpI9FlTiNg",
    "businessname": "Asia Restaurant",
    "address": "8060 Zürich"
  }
  JSON
  ```

- [ ] `e3F-0T3Xi13i3wbcwaW1gg` — NEUMARKT — Neumarkt 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "e3F-0T3Xi13i3wbcwaW1gg",
    "businessname": "NEUMARKT",
    "address": "Neumarkt 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `wFJgnSSK_mdXORsSuFU4Ow` — Safari Bar — Zähringerstrasse 29, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "wFJgnSSK_mdXORsSuFU4Ow",
    "businessname": "Safari Bar",
    "address": "Zähringerstrasse 29, 8001 Zürich"
  }
  JSON
  ```

- [ ] `pgqO7fOemFzKnGLypCkobA` — ZAATAR — Brauerstrasse 74, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pgqO7fOemFzKnGLypCkobA",
    "businessname": "ZAATAR",
    "address": "Brauerstrasse 74, 8004 Zürich"
  }
  JSON
  ```

- [ ] `orMO22woRL6zE5HFGak_Hw` — Jasmin — Herzogenmühlestrasse 4, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "orMO22woRL6zE5HFGak_Hw",
    "businessname": "Jasmin",
    "address": "Herzogenmühlestrasse 4, 8051 Zürich"
  }
  JSON
  ```

- [ ] `1EhTjvzVDTgHUOerpv4ZHA` — Bistrot chez Marion — Mühlegasse 22, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "1EhTjvzVDTgHUOerpv4ZHA",
    "businessname": "Bistrot chez Marion",
    "address": "Mühlegasse 22, 8001 Zürich"
  }
  JSON
  ```

- [ ] `yqd3PvUQPF--7_cia3ZxWw` — Teecafe Schwarzenbach — Münstergasse 17, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yqd3PvUQPF--7_cia3ZxWw",
    "businessname": "Teecafe Schwarzenbach",
    "address": "Münstergasse 17, 8001 Zürich"
  }
  JSON
  ```

- [ ] `6M-i-i4ZvORTXesE2Irrww` — Bauernschänke — Rindermarkt 24, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6M-i-i4ZvORTXesE2Irrww",
    "businessname": "Bauernschänke",
    "address": "Rindermarkt 24, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Gir5T9vd140Qs26YPXl2gw` — Trottoir Gastro — Schöneggstrasse 23, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Gir5T9vd140Qs26YPXl2gw",
    "businessname": "Trottoir Gastro",
    "address": "Schöneggstrasse 23, 8004 Zürich"
  }
  JSON
  ```

- [ ] `3pCLHrmCvlIxDNQH8mhXmw` — Hotel Neufeld — Friesenbergstrasse 15, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3pCLHrmCvlIxDNQH8mhXmw",
    "businessname": "Hotel Neufeld",
    "address": "Friesenbergstrasse 15, 8055 Zürich"
  }
  JSON
  ```

- [ ] `EzVN9HBKEc43JwR8JyEkDg` — SMITH AND DE LUMA — Grubenstrasse 27, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EzVN9HBKEc43JwR8JyEkDg",
    "businessname": "SMITH AND DE LUMA",
    "address": "Grubenstrasse 27, 8045 Zürich"
  }
  JSON
  ```

- [ ] `x8Gsxrp9zMKTjldtpkvHgA` — Hasta Ice Cream — Zwingliplatz 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "x8Gsxrp9zMKTjldtpkvHgA",
    "businessname": "Hasta Ice Cream",
    "address": "Zwingliplatz 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `vlP5mNW6vZeXQlQsHAmcYg` — Piadina Bar — Niederdorfstrasse 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vlP5mNW6vZeXQlQsHAmcYg",
    "businessname": "Piadina Bar",
    "address": "Niederdorfstrasse 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `mosSkISHpvH3HaNwZod9BA` — Morgenstern — Zwinglistrasse 27, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "mosSkISHpvH3HaNwZod9BA",
    "businessname": "Morgenstern",
    "address": "Zwinglistrasse 27, 8004 Zürich"
  }
  JSON
  ```

- [ ] `84xQNlPQXXYwCyV_fCr5jQ` — Hospiz @ Gotthard Bar — Langstrasse 63, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "84xQNlPQXXYwCyV_fCr5jQ",
    "businessname": "Hospiz @ Gotthard Bar",
    "address": "Langstrasse 63, 8004 Zürich"
  }
  JSON
  ```

- [ ] `3yC74CRNya zk7I3_umEFtA` — dean & david ZH Wiesenstrasse — Wiesenstrasse 1, 8008 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3yC74CRNyazk7I3_umEFtA",
    "businessname": "dean & david ZH Wiesenstrasse",
    "address": "Wiesenstrasse 1, 8008 Zürich"
  }
  JSON
  ```

- [ ] `7ozC0bhN9BOLeU-mjrbQSQ` — Burgermeister — Langstrasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7ozC0bhN9BOLeU-mjrbQSQ",
    "businessname": "Burgermeister",
    "address": "Langstrasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `LFUZkOdEC_1D8Z7cjRzg0A` — Capri Pizzeria — Dufourstrasse 80, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "LFUZkOdEC_1D8Z7cjRzg0A",
    "businessname": "Capri Pizzeria",
    "address": "Dufourstrasse 80, 8008 Zürich"
  }
  JSON
  ```

- [ ] `ueGQLQqfvqdhFZyYS9e6qA` — Restaurant Commercio — Mühlebachstrasse 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ueGQLQqfvqdhFZyYS9e6qA",
    "businessname": "Restaurant Commercio",
    "address": "Mühlebachstrasse 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `7LY0U5jTCWP1zYMddSAbFQ` — King Rice Restaurant — Schaffhauserstrasse 413, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7LY0U5jTCWP1zYMddSAbFQ",
    "businessname": "King Rice Restaurant",
    "address": "Schaffhauserstrasse 413, 8050 Zürich"
  }
  JSON
  ```

- [ ] `eFWTFtYlE6c7xxlAb6tM3g` — Griechische Taverne L & P GmbH — Seefeldstrasse 167, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "eFWTFtYlE6c7xxlAb6tM3g",
    "businessname": "Griechische Taverne L & P GmbH",
    "address": "Seefeldstrasse 167, 8008 Zürich"
  }
  JSON
  ```

- [ ] `rX-BqCmt6l4X7fcdNMKnLw` — Dialog — Münstergasse 4, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rX-BqCmt6l4X7fcdNMKnLw",
    "businessname": "Dialog",
    "address": "Münstergasse 4, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gfYcLy5JbtPiUQKRBImiNw` — Exer Gastronomie GmbH — Tellstrasse 10, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gfYcLy5JbtPiUQKRBImiNw",
    "businessname": "Exer Gastronomie GmbH",
    "address": "Tellstrasse 10, 8004 Zürich"
  }
  JSON
  ```

- [ ] `v4Vc7DJWoQxqwAXgOjHYMg` — Giusi's Ristorante Pizzeria — Zollikerstrasse 10, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "v4Vc7DJWoQxqwAXgOjHYMg",
    "businessname": "Giusi's Ristorante Pizzeria",
    "address": "Zollikerstrasse 10, 8008 Zürich"
  }
  JSON
  ```

- [ ] `oAoHm28TDCi_o4zTIPzung` — Restaurant Schlüssel — Seefeldstrasse 177, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "oAoHm28TDCi_o4zTIPzung",
    "businessname": "Restaurant Schlüssel",
    "address": "Seefeldstrasse 177, 8008 Zürich"
  }
  JSON
  ```

- [ ] `AagN-fnvVURHzWaVxadp2Q` — Restaurant/Take Away Tschingg Oberdorf — Oberdorfstrasse 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AagN-fnvVURHzWaVxadp2Q",
    "businessname": "Restaurant/Take Away Tschingg Oberdorf",
    "address": "Oberdorfstrasse 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `N-cXLa7bitDFMl6bsrv6AQ` — Blaue Ente — Seefeldstrasse 223, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "N-cXLa7bitDFMl6bsrv6AQ",
    "businessname": "Blaue Ente",
    "address": "Seefeldstrasse 223, 8008 Zürich"
  }
  JSON
  ```

- [ ] `RImoJQPF5SaOy0zfA6A1yw` — Payamlino Take Away — Uetlibergstrasse 103, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RImoJQPF5SaOy0zfA6A1yw",
    "businessname": "Payamlino Take Away",
    "address": "Uetlibergstrasse 103, 8045 Zürich"
  }
  JSON
  ```

- [ ] `E-kt3FQx08WrWfY4D-CHRA` — Kafi Mümpfeli — Wehntalerstrasse 286, 8046 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "E-kt3FQx08WrWfY4D-CHRA",
    "businessname": "Kafi Mümpfeli",
    "address": "Wehntalerstrasse 286, 8046 Zürich"
  }
  JSON
  ```

- [ ] `5DfzfI3OUGzBz05d0uHOxA` — Petra's Tip-Top-Bar — Seilergraben 13, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5DfzfI3OUGzBz05d0uHOxA",
    "businessname": "Petra's Tip-Top-Bar",
    "address": "Seilergraben 13, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CTERGmSvrYyANpVumRreqA` — PLOY THAI RESTAURANT HONGBIN — Uetlibergstrasse 38, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CTERGmSvrYyANpVumRreqA",
    "businessname": "PLOY THAI RESTAURANT HONGBIN",
    "address": "Uetlibergstrasse 38, 8045 Zürich"
  }
  JSON
  ```

- [ ] `8bMWNcOZlAGPPUkO9Lhj-w` — UBS Restaurant Europaallee — Eisgasse 10, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8bMWNcOZlAGPPUkO9Lhj-w",
    "businessname": "UBS Restaurant Europaallee",
    "address": "Eisgasse 10, 8004 Zürich"
  }
  JSON
  ```

- [ ] `u7GvyqIiO4EJzstcvfY05A` — Weinschenke Hotel Hirschen — Hirschengasse, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "u7GvyqIiO4EJzstcvfY05A",
    "businessname": "Weinschenke Hotel Hirschen",
    "address": "Hirschengasse, 8001 Zürich"
  }
  JSON
  ```

- [ ] `DPaObTzZjYC16zvtRT48DQ` — BACKbAR — Seefeldstrasse 169, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DPaObTzZjYC16zvtRT48DQ",
    "businessname": "BACKbAR",
    "address": "Seefeldstrasse 169, 8008 Zürich"
  }
  JSON
  ```

- [ ] `Z74C2bLqcnEf5-UoFzOR7g` — Accademia Del Gusto — Rotwandstrasse 48, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Z74C2bLqcnEf5-UoFzOR7g",
    "businessname": "Accademia Del Gusto",
    "address": "Rotwandstrasse 48, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nPY8QiOx6XYk7awkdvBPjA` — f39 restaurant — Fröhlichstrasse 39, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nPY8QiOx6XYk7awkdvBPjA",
    "businessname": "f39 restaurant",
    "address": "Fröhlichstrasse 39, 8008 Zürich"
  }
  JSON
  ```

- [ ] `GvAUCMu6sNPf23wAIa87_w` — Restaurant Johanniter — Niederdorfstrasse 70, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GvAUCMu6sNPf23wAIa87_w",
    "businessname": "Restaurant Johanniter",
    "address": "Niederdorfstrasse 70, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HsWouR3P0-dM4u3UtgvTmg` — Itasia — Dufourstrasse 57, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HsWouR3P0-dM4u3UtgvTmg",
    "businessname": "Itasia",
    "address": "Dufourstrasse 57, 8008 Zürich"
  }
  JSON
  ```

- [ ] `IOWTFtTJe_ZkJqSHgL0R9g` — Bar Andorra — Münstergasse 20, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IOWTFtTJe_ZkJqSHgL0R9g",
    "businessname": "Bar Andorra",
    "address": "Münstergasse 20, 8001 Zürich"
  }
  JSON
  ```

- [ ] `5GBj0ilLYS2VFIC3ylpNIg` — Gasthaus Albisgütli — Uetlibergstrasse 341, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5GBj0ilLYS2VFIC3ylpNIg",
    "businessname": "Gasthaus Albisgütli",
    "address": "Uetlibergstrasse 341, 8045 Zürich"
  }
  JSON
  ```

- [ ] `MdCuSADh178WWHMeO8rFgw` — Restaurant Eichhörnli — Nietengasse 16, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "businessname": "Restaurant Eichhörnli",
    "entry_id": "MdCuSADh178WWHMeO8rFgw",
    "address": "Nietengasse 16, 8004 Zürich"
  }
  JSON
  ```

- [ ] `e-OyP8BuRHWa_uFZnWx10Q` — Ban Song Thai — Kirchgasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "e-OyP8BuRHWa_uFZnWx10Q",
    "businessname": "Ban Song Thai",
    "address": "Kirchgasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `PA6qRaKHs613yybiVaaTrw` — Angels Wine Tower Grill — 8058 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "PA6qRaKHs613yybiVaaTrw",
    "businessname": "Angels Wine Tower Grill",
    "address": "8058 Zürich"
  }
  JSON
  ```

- [ ] `tBy5dc1yhXwSlwq1v218AQ` — Burger King — 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "tBy5dc1yhXwSlwq1v218AQ",
    "businessname": "Burger King",
    "address": "8060 Zürich"
  }
  JSON
  ```

- [ ] `3TNm6avPCTluuq9WWQNBOQ` — Pret A Manger Dock E — 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3TNm6avPCTluuq9WWQNBOQ",
    "businessname": "Pret A Manger Dock E",
    "address": "8060 Zürich"
  }
  JSON
  ```

- [ ] `0Z780hMbIiDCtI4asiUOcA` — Sablier - Rooftop Restaurant & Bar — The Circle 23, 8058 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0Z780hMbIiDCtI4asiUOcA",
    "businessname": "Sablier - Rooftop Restaurant & Bar",
    "address": "The Circle 23, 8058 Zürich"
  }
  JSON
  ```

- [ ] `U14r22WSEiXw8DyuwCMdag` — HSV Clubhaus - Der Dorf Treffpunkt — Hagenholzstrasse 81a, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "U14r22WSEiXw8DyuwCMdag",
    "businessname": "HSV Clubhaus - Der Dorf Treffpunkt",
    "address": "Hagenholzstrasse 81a, 8050 Zürich"
  }
  JSON
  ```

- [ ] `MBX6whPF3HxlNwzdQ149WQ` — Avenida — Strassburgstrasse 17, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "MBX6whPF3HxlNwzdQ149WQ",
    "businessname": "Avenida",
    "address": "Strassburgstrasse 17, 8004 Zürich"
  }
  JSON
  ```

- [ ] `lKrPrkJYEfrfXYikXM0IzA` — Babi's Bagel Shop — Bederstrasse 102, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lKrPrkJYEfrfXYikXM0IzA",
    "businessname": "Babi's Bagel Shop",
    "address": "Bederstrasse 102, 8002 Zürich"
  }
  JSON
  ```

- [ ] `JVe1KJ6OE_cO_6AtuU6cPQ` — Flussbad Unterer Letten — Wasserwerkstrasse 131, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JVe1KJ6OE_cO_6AtuU6cPQ",
    "businessname": "Flussbad Unterer Letten",
    "address": "Wasserwerkstrasse 131, 8037 Zürich"
  }
  JSON
  ```

- [ ] `0dmLcpHNerR8vnrHFRoxTQ` — Cafe Presse Club — Münsterhof 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0dmLcpHNerR8vnrHFRoxTQ",
    "businessname": "Cafe Presse Club",
    "address": "Münsterhof 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `G7Fc4ytLyBoDSypUO6P1Jw` — Maison Blunt — Gasometerstrasse 5, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "G7Fc4ytLyBoDSypUO6P1Jw",
    "businessname": "Maison Blunt",
    "address": "Gasometerstrasse 5, 8005 Zürich"
  }
  JSON
  ```

- [ ] `uklnRySCO-Ny0--0R1Qi1w` — Restaurant UniTurm — Rämistrasse 71, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "uklnRySCO-Ny0--0R1Qi1w",
    "businessname": "Restaurant UniTurm",
    "address": "Rämistrasse 71, 8006 Zürich"
  }
  JSON
  ```

- [ ] `IcpUePMDANvvBJYRSlIr0Q` — Riviera Pizzeria — Förrlibuckstrasse 62, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IcpUePMDANvvBJYRSlIr0Q",
    "businessname": "Riviera Pizzeria",
    "address": "Förrlibuckstrasse 62, 8005 Zürich"
  }
  JSON
  ```

- [ ] `sdKK4aYfa5vaW82Vo5mS4Q` — Seerestaurant Badi Wollishofen — Seestrasse 451, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sdKK4aYfa5vaW82Vo5mS4Q",
    "businessname": "Seerestaurant Badi Wollishofen",
    "address": "Seestrasse 451, 8038 Zürich"
  }
  JSON
  ```

- [ ] `kZzNzNAQk4RNLaiXizre3w` — Restaurant Markthalle — Limmatstrasse 231, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kZzNzNAQk4RNLaiXizre3w",
    "businessname": "Restaurant Markthalle",
    "address": "Limmatstrasse 231, 8005 Zürich"
  }
  JSON
  ```

- [ ] `rLyoGfhM5NM0drHXrmSQ9Q` — Kailash Parbat — Claridenstrasse 36, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rLyoGfhM5NM0drHXrmSQ9Q",
    "businessname": "Kailash Parbat",
    "address": "Claridenstrasse 36, 8002 Zürich"
  }
  JSON
  ```

- [ ] `tu-L0BB8ci03-jF74IqGIQ` — Vivid Tapas Bar — Turbinenstrasse 20, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "tu-L0BB8ci03-jF74IqGIQ",
    "businessname": "Vivid Tapas Bar",
    "address": "Turbinenstrasse 20, 8005 Zürich"
  }
  JSON
  ```

- [ ] `nOrmUgn0CexqiVfwq6pcJA` — O'Callaghan's Shamrock Pub — Studackerstrasse 1, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nOrmUgn0CexqiVfwq6pcJA",
    "businessname": "O'Callaghan's Shamrock Pub",
    "address": "Studackerstrasse 1, 8038 Zürich"
  }
  JSON
  ```

- [ ] `I5QK2jj8qQbfqfMsts11nA` — RAW by Michael Adams — Ackerstrasse 56, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "I5QK2jj8qQbfqfMsts11nA",
    "businessname": "RAW by Michael Adams",
    "address": "Ackerstrasse 56, 8005 Zürich"
  }
  JSON
  ```

- [ ] `DoKUXpc7 zHomXPxvHN6t5g` — Restaurant Am Brühlbach — Kappenbühlweg 11, 8049 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DoKUXpc7 zHomXPxvHN6t5g",
    "businessname": "Restaurant Am Brühlbach",
    "address": "Kappenbühlweg 11, 8049 Zürich"
  }
  JSON
  ```

- [ ] `2vqwOYl3jaOuV1bHFmomJQ` — Devi Deli Göttlich Vegan — Bertastrasse 11, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2vqwOYl3jaOuV1bHFmomJQ",
    "businessname": "Devi Deli Göttlich Vegan",
    "address": "Bertastrasse 11, 8003 Zürich"
  }
  JSON
  ```

- [ ] `FhL_m63EYtSnSEQfSzJqtw` — Mercure Hotel Stoller Zürich — Badenerstrasse 357, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FhL_m63EYtSnSEQfSzJqtw",
    "businessname": "Mercure Hotel Stoller Zürich",
    "address": "Badenerstrasse 357, 8003 Zürich"
  }
  JSON
  ```

- [ ] `VXHbU99j5ci8v4iY3qQYyA` — Il Pantheon — Limmattalstrasse 400, 8049 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VXHbU99j5ci8v4iY3qQYyA",
    "businessname": "Il Pantheon",
    "address": "Limmattalstrasse 400, 8049 Zürich"
  }
  JSON
  ```

- [ ] `kNu1IG-2OZV_zI2Z3ypQaA` — Billiardino — Heinrichstrasse 245, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kNu1IG-2OZV_zI2Z3ypQaA",
    "businessname": "Billiardino",
    "address": "Heinrichstrasse 245, 8005 Zürich"
  }
  JSON
  ```

- [ ] `u_aMz7r27vS7QrtMJj3Ppw` — Wesley's Kitchen — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "u_aMz7r27vS7QrtMJj3Ppw",
    "businessname": "Wesley's Kitchen",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `r7BdEQ1dyS9j2CSp6Hhs_w` — Babo's Restaurant — Langstrasse 192, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "r7BdEQ1dyS9j2CSp6Hhs_w",
    "businessname": "Babo's Restaurant",
    "address": "Langstrasse 192, 8005 Zürich"
  }
  JSON
  ```

- [ ] `dq43HWfMEJPDSH-R7eaO7w` — Zest of Asia — Luisenstrasse 43, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dq43HWfMEJPDSH-R7eaO7w",
    "businessname": "Zest of Asia",
    "address": "Luisenstrasse 43, 8005 Zürich"
  }
  JSON
  ```

- [ ] `HJZuur1BKpgniXIU5LbtYw` — Restaurant Yan-Ruyi — Albisstrasse 19, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HJZuur1BKpgniXIU5LbtYw",
    "businessname": "Restaurant Yan-Ruyi",
    "address": "Albisstrasse 19, 8038 Zürich"
  }
  JSON
  ```

- [ ] `7MuWaGquV3CCK9ODPFldmQ` — Thali House Indian Restaurant — Langstrasse 213, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7MuWaGquV3CCK9ODPFldmQ",
    "businessname": "Thali House Indian Restaurant",
    "address": "Langstrasse 213, 8005 Zürich"
  }
  JSON
  ```

- [ ] `RP7addpBrHPOJczUzOYvkA` — The Lemon Grass Thai Take Away & Catering — Limmatstrasse 199, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RP7addpBrHPOJczUzOYvkA",
    "businessname": "The Lemon Grass Thai Take Away & Catering",
    "address": "Limmatstrasse 199, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Gu1VJWFRJ3ivHDiBYJ89TA` — Pizzeria Antonio — Hardturmstrasse 133, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Gu1VJWFRJ3ivHDiBYJ89TA",
    "businessname": "Pizzeria Antonio",
    "address": "Hardturmstrasse 133, 8005 Zürich"
  }
  JSON
  ```

- [ ] `YNIuUXqIpI3BJQAX6GcqxQ` — Noona — Albisstrasse 107, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "YNIuUXqIpI3BJQAX6GcqxQ",
    "businessname": "Noona",
    "address": "Albisstrasse 107, 8038 Zürich"
  }
  JSON
  ```

- [ ] `Xq--O7RXbpPJH5Fhu_DOIg` — ONA POKÉ AG — Lintheschergasse 13, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Xq--O7RXbpPJH5Fhu_DOIg",
    "businessname": "ONA POKÉ AG",
    "address": "Lintheschergasse 13, 8001 Zürich"
  }
  JSON
  ```

- [ ] `DsGXp4OnbN2A5S13luZP8Q` — Café du Centenaire — Badenerstrasse 571, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DsGXp4OnbN2A5S13luZP8Q",
    "businessname": "Café du Centenaire",
    "address": "Badenerstrasse 571, 8048 Zürich"
  }
  JSON
  ```

- [ ] `7RKDv6WFWWNnsUYeKG2vUg` — Magoosh Grill - Restaurant - Bar — Stampfenbachstrasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7RKDv6WFWWNnsUYeKG2vUg",
    "businessname": "Magoosh Grill - Restaurant - Bar",
    "address": "Stampfenbachstrasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `vO07-PdHr_vlyRPoUUHeGw` — Fujiya of Japan — Tessinerplatz 5, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vO07-PdHr_vlyRPoUUHeGw",
    "businessname": "Fujiya of Japan",
    "address": "Tessinerplatz 5, 8002 Zürich"
  }
  JSON
  ```

- [ ] `trU5ncCqMf8qtseYfA2v2w` — Arogyam — Badenerstrasse 298, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "trU5ncCqMf8qtseYfA2v2w",
    "businessname": "Arogyam",
    "address": "Badenerstrasse 298, 8004 Zürich"
  }
  JSON
  ```

- [ ] `YjVylVPPIzYb3Gszc64FtQ` — Cucina Milchbuck — Schaffhauserstrasse 113, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "YjVylVPPIzYb3Gszc64FtQ",
    "businessname": "Cucina Milchbuck",
    "address": "Schaffhauserstrasse 113, 8057 Zürich"
  }
  JSON
  ```

- [ ] `5vX6l1QaIeaiyozekTgEdQ` — Urban Fork — Ackerstrasse 56, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5vX6l1QaIeaiyozekTgEdQ",
    "businessname": "Urban Fork",
    "address": "Ackerstrasse 56, 8005 Zürich"
  }
  JSON
  ```

- [ ] `ckuetyLZQJfhfF45W0s7_g` — Genovas Fine Food & Beverage — Bertastrasse 26, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ckuetyLZQJfhfF45W0s7_g",
    "businessname": "Genovas Fine Food & Beverage",
    "address": "Bertastrasse 26, 8003 Zürich"
  }
  JSON
  ```

- [ ] `-6tlhQ5q6U9tq4xVLNAIkg` — Ristorante Italia — Witikonerstrasse 289, 8053 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-6tlhQ5q6U9tq4xVLNAIkg",
    "businessname": "Ristorante Italia",
    "address": "Witikonerstrasse 289, 8053 Zürich"
  }
  JSON
  ```

- [ ] `bWkcnzb6WmG5YBMWPMkNYA` — Café Bebek AG — Badenerstrasse 171, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "bWkcnzb6WmG5YBMWPMkNYA",
    "businessname": "Café Bebek AG",
    "address": "Badenerstrasse 171, 8003 Zürich"
  }
  JSON
  ```

- [ ] `ZolGiJcaVYAdfhA-MW-CJw` — Quartier 5 — Hardturmstrasse 126A, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZolGiJcaVYAdfhA-MW-CJw",
    "businessname": "Quartier 5",
    "address": "Hardturmstrasse 126A, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Tibq2KtHTc0Ti1iiNjpAFA` — Belvoirpark Restaurant — Seestrasse 125, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Tibq2KtHTc0Ti1iiNjpAFA",
    "businessname": "Belvoirpark Restaurant",
    "address": "Seestrasse 125, 8002 Zürich"
  }
  JSON
  ```

- [ ] `dRV7z6MMgOSBac1z3SVJpA` — Albis Beck Café Frankental — Konrad-Ilg-Strasse 4, 8049 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dRV7z6MMgOSBac1z3SVJpA",
    "businessname": "Albis Beck Café Frankental",
    "address": "Konrad-Ilg-Strasse 4, 8049 Zürich"
  }
  JSON
  ```

- [ ] `cZr8m11TJi8M5PQGBeQhTQ` — By Khalid Mexican Restaurant — Schaffhauserstrasse 116, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cZr8m11TJi8M5PQGBeQhTQ",
    "businessname": "By Khalid Mexican Restaurant",
    "address": "Schaffhauserstrasse 116, 8057 Zürich"
  }
  JSON
  ```

- [ ] `VqKL_iUYh9ySJc6eMQ40Zw` — Backerei Hug — Stauffacherstrasse 28, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VqKL_iUYh9ySJc6eMQ40Zw",
    "businessname": "Backerei Hug",
    "address": "Stauffacherstrasse 28, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Qvhhxfj_G1aO8X1bx8W_tQ` — Starbucks Coffee House — Limmatstrasse 5, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Qvhhxfj_G1aO8X1bx8W_tQ",
    "businessname": "Starbucks Coffee House",
    "address": "Limmatstrasse 5, 8005 Zürich"
  }
  JSON
  ```

- [ ] `CIwgWvgGsenhtGZZucDIxA` — Pizza Kebab Lochergut — Badenerstrasse 213, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CIwgWvgGsenhtGZZucDIxA",
    "businessname": "Pizza Kebab Lochergut",
    "address": "Badenerstrasse 213, 8003 Zürich"
  }
  JSON
  ```

- [ ] `uRuFyD17pCKt0C5TbT9sHg` — 3 Brüder Ristorante Pizzeria GmbH — Limmatstrasse 125, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "uRuFyD17pCKt0C5TbT9sHg",
    "businessname": "3 Brüder Ristorante Pizzeria GmbH",
    "address": "Limmatstrasse 125, 8005 Zürich"
  }
  JSON
  ```

- [ ] `B07OyPgQ9m0xT-q6_yMaCQ` — Tadka Restaurant — Quellenstrasse 49, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "B07OyPgQ9m0xT-q6_yMaCQ",
    "businessname": "Tadka Restaurant",
    "address": "Quellenstrasse 49, 8005 Zürich"
  }
  JSON
  ```

- [ ] `ihvRQpopNz8RmREVl2K8oA` — Restaurant Medina — Albisstrasse 72, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ihvRQpopNz8RmREVl2K8oA",
    "businessname": "Restaurant Medina",
    "address": "Albisstrasse 72, 8038 Zürich"
  }
  JSON
  ```

- [ ] `4XXX9RX9y_etvLg7BLFK7w` — Fein und Schein — Schöntalstrasse 14, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4XXX9RX9y_etvLg7BLFK7w",
    "businessname": "Fein und Schein",
    "address": "Schöntalstrasse 14, 8004 Zürich"
  }
  JSON
  ```

- [ ] `_G66OOCKSeOjO2JWkr6aNA` — Kulturmarkt — Aemtlerstrasse 23, 8003 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_G66OOCKSeOjO2JWkr6aNA",
    "businessname": "Kulturmarkt",
    "address": "Aemtlerstrasse 23, 8003 Zürich"
  }
  JSON
  ```

- [ ] `6tMwkhf3d0TsUzHrAhs2MQ` — Bar Enge — Seestrasse 7, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6tMwkhf3d0TsUzHrAhs2MQ",
    "businessname": "Bar Enge",
    "address": "Seestrasse 7, 8002 Zürich"
  }
  JSON
  ```

- [ ] `krfYQCaiIOd4UDf3owHtRg` — Burgers & Shakes — Birmensdorferstrasse 430, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "krfYQCaiIOd4UDf3owHtRg",
    "businessname": "Burgers & Shakes",
    "address": "Birmensdorferstrasse 430, 8055 Zürich"
  }
  JSON
  ```

- [ ] `M8NQIbdqvZQTFGFmQZOjyA` — Hermanseck — Birmensdorferstrasse 58, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "M8NQIbdqvZQTFGFmQZOjyA",
    "businessname": "Hermanseck",
    "address": "Birmensdorferstrasse 58, 8004 Zürich"
  }
  JSON
  ```

- [ ] `055jLpexaW3agQfdjrF3bQ` — El Luchador — Konradstrasse 69, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "055jLpexaW3agQfdjrF3bQ",
    "businessname": "El Luchador",
    "address": "Konradstrasse 69, 8005 Zürich"
  }
  JSON
  ```

- [ ] `HhOfN0EBw5B6zKcjrsLigg` — Vee's Bistro — Alfred-Escher-Strasse 11, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HhOfN0EBw5B6zKcjrsLigg",
    "businessname": "Vee's Bistro",
    "address": "Alfred-Escher-Strasse 11, 8002 Zürich"
  }
  JSON
  ```

- [ ] `6UEeG987MoId-zHEOekh-w` — Konditorei Berner — Hottingerstrasse 33, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6UEeG987MoId-zHEOekh-w",
    "businessname": "Konditorei Berner",
    "address": "Hottingerstrasse 33, 8032 Zürich"
  }
  JSON
  ```

- [ ] `ECXCEQAr8Jectlh3bv6Emw` — Nooba — Kreuzplatz 5, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ECXCEQAr8Jectlh3bv6Emw",
    "businessname": "Nooba",
    "address": "Kreuzplatz 5, 8032 Zürich"
  }
  JSON
  ```

- [ ] `OEzwTbNFoiGZXYtSLMsVLg` — ViCOLLECTIVE AG — Zollstrasse 117, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OEzwTbNFoiGZXYtSLMsVLg",
    "businessname": "ViCOLLECTIVE AG",
    "address": "Zollstrasse 117, 8005 Zürich"
  }
  JSON
  ```

- [ ] `ANZe4U_M5uu7FlqMQMscxg` — Ruenthai 2 Take Away — Badenerstrasse 582, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ANZe4U_M5uu7FlqMQMscxg",
    "businessname": "Ruenthai 2 Take Away",
    "address": "Badenerstrasse 582, 8048 Zürich"
  }
  JSON
  ```

- [ ] `-Lf_fuI1Bqq-sOFpDJNcdQ` — Reblaube — Glockengasse 7, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-Lf_fuI1Bqq-sOFpDJNcdQ",
    "businessname": "Reblaube",
    "address": "Glockengasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `vJU4Ynylo36in_jnsAEHvQ` — Restaurant Bar Café Ey Hof — Triemlistrasse 183, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vJU4Ynylo36in_jnsAEHvQ",
    "businessname": "Restaurant Bar Café Ey Hof",
    "address": "Triemlistrasse 183, 8047 Zürich"
  }
  JSON
  ```

- [ ] `kWFxqQl8Q_nIMZZfyi7lkQ` — Royal Panda — Forchstrasse 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kWFxqQl8Q_nIMZZfyi7lkQ",
    "businessname": "Royal Panda",
    "address": "Forchstrasse 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `i3tFjsOmQRgxOfHcavCLGw` — Waiana Tiki Bar — Glockengasse 7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "i3tFjsOmQRgxOfHcavCLGw",
    "businessname": "Waiana Tiki Bar",
    "address": "Glockengasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gKvvfk-Oh9_KZKFaHsWM6Q` — Läderach Chocolatier Suisse — Bahnhofstrasse 106, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gKvvfk-Oh9_KZKFaHsWM6Q",
    "businessname": "Läderach Chocolatier Suisse",
    "address": "Bahnhofstrasse 106, 8001 Zürich"
  }
  JSON
  ```

- [ ] `ULVQ4eQlr8jDUTsV7umeJQ` — Cafe Altstetten — Altstetterstrasse 130, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ULVQ4eQlr8jDUTsV7umeJQ",
    "businessname": "Cafe Altstetten",
    "address": "Altstetterstrasse 130, 8048 Zürich"
  }
  JSON
  ```

- [ ] `ndZWID4LZBOBVUighSd1NA` — Bäckerei & Konditorei - Café Peter — Tramstrasse 235, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ndZWID4LZBOBVUighSd1NA",
    "businessname": "Bäckerei & Konditorei - Café Peter",
    "address": "Tramstrasse 235, 8050 Zürich"
  }
  JSON
  ```

- [ ] `U4ntcBopbywljkUmckUYtQ` — Cantinetta Antinori — Augustinergasse 25, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "U4ntcBopbywljkUmckUYtQ",
    "businessname": "Cantinetta Antinori",
    "address": "Augustinergasse 25, 8001 Zürich"
  }
  JSON
  ```

- [ ] `xT7HR7SUxerL2v7h_UrRVA` — Foodpoint Restaurant — Kreuzplatz 8008, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xT7HR7SUxerL2v7h_UrRVA",
    "businessname": "Foodpoint Restaurant",
    "address": "Kreuzplatz 8008, 8008 Zürich"
  }
  JSON
  ```

- [ ] `ZuUbImxGu5VzqIBPaproZQ` — Cafeteria BS für Detailhandel - Niklausstrasse — Niklausstrasse 16, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZuUbImxGu5VzqIBPaproZQ",
    "businessname": "Cafeteria BS für Detailhandel - Niklausstrasse",
    "address": "Niklausstrasse 16, 8006 Zürich"
  }
  JSON
  ```

- [ ] `RsDHsOEBKgcQmuDhZ6ayBQ` — ZAWAN Thai Kitchen — Rigiplatz 1, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RsDHsOEBKgcQmuDhZ6ayBQ",
    "businessname": "ZAWAN Thai Kitchen",
    "address": "Rigiplatz 1, 8006 Zürich"
  }
  JSON
  ```

- [ ] `5A-dhdQR4Tw_1vw1eXv0iw` — Restaurant Pizza Züri — Badenerstrasse 558, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5A-dhdQR4Tw_1vw1eXv0iw",
    "businessname": "Restaurant Pizza Züri",
    "address": "Badenerstrasse 558, 8048 Zürich"
  }
  JSON
  ```

- [ ] `tcTpNO9hdh6R2-XdIoUKSQ` — Burger King — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "tcTpNO9hdh6R2-XdIoUKSQ",
    "businessname": "Burger King",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `VEcAPmtyf0aLs-LP_XRRBg` — Gabbani Zürich — Talstrasse 40, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VEcAPmtyf0aLs-LP_XRRBg",
    "businessname": "Gabbani Zürich",
    "address": "Talstrasse 40, 8001 Zürich"
  }
  JSON
  ```

- [ ] `tzLqbCd_xSOGmC_VbGcr_w` — Mövenpick Ice Cream Gallery — Theaterstrasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "tzLqbCd_xSOGmC_VbGcr_w",
    "businessname": "Mövenpick Ice Cream Gallery",
    "address": "Theaterstrasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CB1WJYis4gm8EtlEFWmvIg` — Ali Osman Engin — Wallisellenstrasse 5, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CB1WJYis4gm8EtlEFWmvIg",
    "businessname": "Ali Osman Engin",
    "address": "Wallisellenstrasse 5, 8050 Zürich"
  }
  JSON
  ```

- [ ] `WuCiA-7Bvi25iGpGLAJqCg` — Hiltl Akademie — Sihlstrasse 24, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "WuCiA-7Bvi25iGpGLAJqCg",
    "businessname": "Hiltl Akademie",
    "address": "Sihlstrasse 24, 8001 Zürich"
  }
  JSON
  ```

- [ ] `lonh-3XCzgCii0hqIqORng` — Konrad — Lintheschergasse 23, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lonh-3XCzgCii0hqIqORng",
    "businessname": "Konrad",
    "address": "Lintheschergasse 23, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CXdD-G1NXEJP9vy9fSU32w` — Black Tap Craft Burgers And Beer — Werdmühlestrasse 4, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CXdD-G1NXEJP9vy9fSU32w",
    "businessname": "Black Tap Craft Burgers And Beer",
    "address": "Werdmühlestrasse 4, 8001 Zürich"
  }
  JSON
  ```

- [ ] `ubAA9IL3FCfUdAhAUAogsQ` — La Bottega di Mario — Nüschelerstrasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ubAA9IL3FCfUdAhAUAogsQ",
    "businessname": "La Bottega di Mario",
    "address": "Nüschelerstrasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `X2CHbjTzwcLws7m4EUKoQQ` — Michelangelo — Gertrudstrasse 37, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "X2CHbjTzwcLws7m4EUKoQQ",
    "businessname": "Michelangelo",
    "address": "Gertrudstrasse 37, 8003 Zürich"
  }
  JSON
  ```

- [ ] `kdgDBy0uJFKOQNm7Fqa_bA` — Osso — Zollstrasse 121, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kdgDBy0uJFKOQNm7Fqa_bA",
    "businessname": "Osso",
    "address": "Zollstrasse 121, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Dzt8_2Mmh_EMz_Rc8Sia1A` — ooo Rooftop Restaurant — Bahnhofstrasse 74, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Dzt8_2Mmh_EMz_Rc8Sia1A",
    "businessname": "ooo Rooftop Restaurant",
    "address": "Bahnhofstrasse 74, 8001 Zürich"
  }
  JSON
  ```

- [ ] `O4VqYsdSUSChocHn0H8LSA` — Die Waid — Waidbadstrasse 45, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "O4VqYsdSUSChocHn0H8LSA",
    "businessname": "Die Waid",
    "address": "Waidbadstrasse 45, 8037 Zürich"
  }
  JSON
  ```

- [ ] `wSj_UXGtjHLAnL4feZPvUA` — Starbucks — Museumstrasse 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "wSj_UXGtjHLAnL4feZPvUA",
    "businessname": "Starbucks",
    "address": "Museumstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `YzHhCosKtfGxh65TF0SzTA` — Gelatissimo — Gessnerallee 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "YzHhCosKtfGxh65TF0SzTA",
    "businessname": "Gelatissimo",
    "address": "Gessnerallee 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CveqVhKXpGSvBxa1PYHLMA` — Hot Pasta AG — Universitätstrasse 15, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CveqVhKXpGSvBxa1PYHLMA",
    "businessname": "Hot Pasta AG",
    "address": "Universitätstrasse 15, 8006 Zürich"
  }
  JSON
  ```

- [ ] `_dYXEVIJFpG9LpJDqJCGLA` — Arctic Juice & Cafe — Sihlstrasse 20, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_dYXEVIJFpG9LpJDqJCGLA",
    "businessname": "Arctic Juice & Cafe",
    "address": "Sihlstrasse 20, 8001 Zürich"
  }
  JSON
  ```

- [ ] `5p7CuLdBmtiXpZse2kYAlQ` — Zum Frischen Max — Max-Frisch-Platz 25a, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5p7CuLdBmtiXpZse2kYAlQ",
    "businessname": "Zum Frischen Max",
    "address": "Max-Frisch-Platz 25a, 8050 Zürich"
  }
  JSON
  ```

- [ ] `AVbXT_bKjdCd8sjZYZMSPQ` — cc.café — Hohlstrasse 484, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AVbXT_bKjdCd8sjZYZMSPQ",
    "businessname": "cc.café",
    "address": "Hohlstrasse 484, 8048 Zürich"
  }
  JSON
  ```

- [ ] `CvBHaAFSJ5uivDXOdi6rtQ` — Wirtschaft zum Transit — Aargauerstrasse 14, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CvBHaAFSJ5uivDXOdi6rtQ",
    "businessname": "Wirtschaft zum Transit",
    "address": "Aargauerstrasse 14, 8048 Zürich"
  }
  JSON
  ```

- [ ] `CNwWZ7kxZq8_ixz6omRjsQ` — Pizzeria Libero — Badenerstrasse 451, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CNwWZ7kxZq8_ixz6omRjsQ",
    "businessname": "Pizzeria Libero",
    "address": "Badenerstrasse 451, 8003 Zürich"
  }
  JSON
  ```

- [ ] `9nfYE0OMQlh5EzxHhvho0w` — Santa Lucia Paradeplatz — Waaggasse 5-7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "9nfYE0OMQlh5EzxHhvho0w",
    "businessname": "Santa Lucia Paradeplatz",
    "address": "Waaggasse 5-7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `v9uQDSkqzrpmytTb19aBJw` — Manuel's — Löwenstrasse 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "v9uQDSkqzrpmytTb19aBJw",
    "businessname": "Manuel's",
    "address": "Löwenstrasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `sTIglrfiv3rIiX_0TiiYWw` — Restaurant 8048 — Lindenplatz 5, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sTIglrfiv3rIiX_0TiiYWw",
    "businessname": "Restaurant 8048",
    "address": "Lindenplatz 5, 8048 Zürich"
  }
  JSON
  ```

- [ ] `FaLRvl8vJEq9028umUMsQw` — Restaurant Time Out — Hirschengraben 64, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FaLRvl8vJEq9028umUMsQw",
    "businessname": "Restaurant Time Out",
    "address": "Hirschengraben 64, 8001 Zürich"
  }
  JSON
  ```

- [ ] `xRV-YXmIRa13Nwd87zVPTg` — James Joyce — Pelikanstrasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xRV-YXmIRa13Nwd87zVPTg",
    "businessname": "James Joyce",
    "address": "Pelikanstrasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `goUBgR08jM_gXZLyqrZnfg` — Indisches Restaurant Kormasutra — Altstetterstrasse 130, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "goUBgR08jM_gXZLyqrZnfg",
    "businessname": "Indisches Restaurant Kormasutra",
    "address": "Altstetterstrasse 130, 8048 Zürich"
  }
  JSON
  ```

- [ ] `_7bXbVBKsmKOszhS7QPZfQ` — Restaurant Heugümper — Waaggasse 4, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_7bXbVBKsmKOszhS7QPZfQ",
    "businessname": "Restaurant Heugümper",
    "address": "Waaggasse 4, 8001 Zürich"
  }
  JSON
  ```

- [ ] `zfXw0TNSbqx9IptcpS9q8A` — Bierhalle Kropf — In Gassen 16, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zfXw0TNSbqx9IptcpS9q8A",
    "businessname": "Bierhalle Kropf",
    "address": "In Gassen 16, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gxxbFik5Qo-PUJKdrQ9yCQ` — Justus — Asylstrasse 70, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gxxbFik5Qo-PUJKdrQ9yCQ",
    "businessname": "Justus",
    "address": "Asylstrasse 70, 8032 Zürich"
  }
  JSON
  ```

- [ ] `ib6RKssr9YBBb_K5vcJ8kw` — QQ Sushi Zürich — Stampfenbachstrasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ib6RKssr9YBBb_K5vcJ8kw",
    "businessname": "QQ Sushi Zürich",
    "address": "Stampfenbachstrasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `_goZB0nLkK0act-IB5Qz5Q` — Collana Bar e Caffè — Theaterstrasse 9, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_goZB0nLkK0act-IB5Qz5Q",
    "businessname": "Collana Bar e Caffè",
    "address": "Theaterstrasse 9, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HmAbMppuEFoAso9Oy2HkMA` — Piazzetta — Bahnhofstrasse 87, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HmAbMppuEFoAso9Oy2HkMA",
    "businessname": "Piazzetta",
    "address": "Bahnhofstrasse 87, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Jy-ULP8UsyODWXEGCC8CxQ` — Restaurant Elefant — Witikonerstrasse 279, 8053 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Jy-ULP8UsyODWXEGCC8CxQ",
    "businessname": "Restaurant Elefant",
    "address": "Witikonerstrasse 279, 8053 Zürich"
  }
  JSON
  ```

- [ ] `q3t5nGUXRb3ZNJq49fLusA` — Not guilty Gastronomie AG — Emil-Oprecht-Strasse 1, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "q3t5nGUXRb3ZNJq49fLusA",
    "businessname": "Not guilty Gastronomie AG",
    "address": "Emil-Oprecht-Strasse 1, 8050 Zürich"
  }
  JSON
  ```

- [ ] `ZDoxMpUHWJgDpI-NhcA5pQ` — Ali Osman Engin — Wallisellenstrasse 5, 80 50 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZDoxMpUHWJgDpI-NhcA5pQ",
    "businessname": "Ali Osman Engin",
    "address": "Wallisellenstrasse 5, 80 50 Zürich"
  }
  JSON
  ```

- [ ] `zNylkLrISlGc1qbqeP742w` — Palette Restaurant Café Bar — Schützengasse 7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zNylkLrISlGc1qbqeP742w",
    "businessname": "Palette Restaurant Café Bar",
    "address": "Schützengasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `NPcu-YOtUZUucLtf_TuCJA` — Indojaya GmbH — Schaffhauserstrasse 373, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "NPcu-YOtUZUucLtf_TuCJA",
    "businessname": "Indojaya GmbH",
    "address": "Schaffhauserstrasse 373, 8050 Zürich"
  }
  JSON
  ```

- [ ] `WrpF74bGPnuuJM8t5ghytg` — Restaurant Ö — Schaffhauserstrasse 335, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "WrpF74bGPnuuJM8t5ghytg",
    "businessname": "Restaurant Ö",
    "address": "Schaffhauserstrasse 335, 8050 Zürich"
  }
  JSON
  ```

- [ ] `IM4nufmoQ1LGNCgYgpCs8w` — Metzgerhalle — Schaffhauserstrasse 354, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IM4nufmoQ1LGNCgYgpCs8w",
    "businessname": "Metzgerhalle",
    "address": "Schaffhauserstrasse 354, 8050 Zürich"
  }
  JSON
  ```

- [ ] `qCI6i8wWIPBPXro_2Ugjag` — Restaurant Riedbach — Hagenholzstrasse 104A, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qCI6i8wWIPBPXro_2Ugjag",
    "businessname": "Restaurant Riedbach",
    "address": "Hagenholzstrasse 104A, 8050 Zürich"
  }
  JSON
  ```

- [ ] `KliQpHZXv6GKc9dzMjoWww` — China-Restaurant King To — Badenerstrasse 816, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KliQpHZXv6GKc9dzMjoWww",
    "businessname": "China-Restaurant King To",
    "address": "Badenerstrasse 816, 8048 Zürich"
  }
  JSON
  ```

- [ ] `iJSv9hNWUtnKWi4vuKxxVQ` — Nooch Asian Kitchen Zürich Badenerstrasse — Badenerstrasse 101, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "iJSv9hNWUtnKWi4vuKxxVQ",
    "businessname": "Nooch Asian Kitchen Zürich Badenerstrasse",
    "address": "Badenerstrasse 101, 8004 Zürich"
  }
  JSON
  ```

- [ ] `HguAJpNl911s21ieYcWC3w` — Restaurant Viadukt — Viaduktstrasse 69, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HguAJpNl911s21ieYcWC3w",
    "businessname": "Restaurant Viadukt",
    "address": "Viaduktstrasse 69, 8005 Zürich"
  }
  JSON
  ```

- [ ] `q9H8zaq1sx4Mew_KLmXlVQ` — Michelle's Cupcakes — Luisenstrasse 19, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "q9H8zaq1sx4Mew_KLmXlVQ",
    "businessname": "Michelle's Cupcakes",
    "address": "Luisenstrasse 19, 8005 Zürich"
  }
  JSON
  ```

- [ ] `3x-F1j_SKhQ2PVCnF9yz0g` — Tritt Käse im Viadukt AG — Limmatstrasse 231, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3x-F1j_SKhQ2PVCnF9yz0g",
    "businessname": "Tritt Käse im Viadukt AG",
    "address": "Limmatstrasse 231, 8005 Zürich"
  }
  JSON
  ```

- [ ] `y3p6HMFOtNOUYUwgMTbQVA` — Restaurant Fischerstube — Bellerivestrasse 160, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "y3p6HMFOtNOUYUwgMTbQVA",
    "businessname": "Restaurant Fischerstube",
    "address": "Bellerivestrasse 160, 8008 Zürich"
  }
  JSON
  ```

- [ ] `QnwubNPSPyuLP_1jcOtOHQ` — O'k Gemüsedöner — Freilagerstrasse 11, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "QnwubNPSPyuLP_1jcOtOHQ",
    "businessname": "O'k Gemüsedöner",
    "address": "Freilagerstrasse 11, 8047 Zürich"
  }
  JSON
  ```

- [ ] `yP-bg9Athx197F_gTlGa0g` — Sternen — Albisriederstrasse 371, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yP-bg9Athx197F_gTlGa0g",
    "businessname": "Sternen",
    "address": "Albisriederstrasse 371, 8047 Zürich"
  }
  JSON
  ```

- [ ] `ZBEldLCcod25V-KY3KLs7g` — Bistro Albisrieden — Albisriederstrasse 358, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZBEldLCcod25V-KY3KLs7g",
    "businessname": "Bistro Albisrieden",
    "address": "Albisriederstrasse 358, 8047 Zürich"
  }
  JSON
  ```

- [ ] `yAD2v7nsKY_yCPaEMHj9wg` — Grainglow Gmbh — Albisriederstrasse 253, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yAD2v7nsKY_yCPaEMHj9wg",
    "businessname": "Grainglow Gmbh",
    "address": "Albisriederstrasse 253, 8047 Zürich"
  }
  JSON
  ```

- [ ] `uYq0jLI3OwJFFN8P2jxX-g` — Spaghetti Factory Rosenhof — Niederdorfstrasse 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "uYq0jLI3OwJFFN8P2jxX-g",
    "businessname": "Spaghetti Factory Rosenhof",
    "address": "Niederdorfstrasse 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `qnilEbBpz5djc3P2ngHs3g` — Test_Nast — H 120, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qnilEbBpz5djc3P2ngHs3g",
    "businessname": "Test_Nast",
    "address": "H 120, 8005 Zürich"
  }
  JSON
  ```

- [ ] `pUTWWiCNQ1hmBIsnvzQMRA` — Zimmi's Bistro — Schaffhauserstrasse 433, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pUTWWiCNQ1hmBIsnvzQMRA",
    "businessname": "Zimmi's Bistro",
    "address": "Schaffhauserstrasse 433, 8050 Zürich"
  }
  JSON
  ```

- [ ] `ygsSP5TRDS5gtxhSi0Cj3g` — Bongusto Cookies & Ice Cream — Niederdorfstrasse 37, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ygsSP5TRDS5gtxhSi0Cj3g",
    "businessname": "Bongusto Cookies & Ice Cream",
    "address": "Niederdorfstrasse 37, 8001 Zürich"
  }
  JSON
  ```

- [ ] `wFA4lXLT-N8s-ydfRlNFoQ` — Brooklyn Burger — Kasernenstrasse 77B, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "wFA4lXLT-N8s-ydfRlNFoQ",
    "businessname": "Brooklyn Burger",
    "address": "Kasernenstrasse 77B, 8004 Zürich"
  }
  JSON
  ```

- [ ] `h7rLuZCoSJoNRneiTLm1Aw` — Bäckerei Konditorei Tanner — Schaffhauserstrasse 427, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "h7rLuZCoSJoNRneiTLm1Aw",
    "businessname": "Bäckerei Konditorei Tanner",
    "address": "Schaffhauserstrasse 427, 8050 Zürich"
  }
  JSON
  ```

- [ ] `lukKwp0EoQhkZ6IzGd5yXA` — Enzian Cafébar — Thurgauerstrasse 36, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lukKwp0EoQhkZ6IzGd5yXA",
    "businessname": "Enzian Cafébar",
    "address": "Thurgauerstrasse 36, 8050 Zürich"
  }
  JSON
  ```

- [ ] `6sfIkSZBtHXCH3tKU1X6KA` — McDonald's — Niederdorfstrasse 30, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6sfIkSZBtHXCH3tKU1X6KA",
    "businessname": "McDonald's",
    "address": "Niederdorfstrasse 30, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Jh7-KB9kNclA-a39dBTy8A` — Williams ButchersTable Bellevue — Schifflände 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Jh7-KB9kNclA-a39dBTy8A",
    "businessname": "Williams ButchersTable Bellevue",
    "address": "Schifflände 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `njmQVlbFG8GV407YfD23SA` — Yi Long Asia Restaurant — Magnusstrasse 16, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "njmQVlbFG8GV407YfD23SA",
    "businessname": "Yi Long Asia Restaurant",
    "address": "Magnusstrasse 16, 8004 Zürich"
  }
  JSON
  ```

- [ ] `QJ_R6pZx1s91PhXS2xnhag` — Mensa FKSZ — Kreuzbühlstrasse 16, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "QJ_R6pZx1s91PhXS2xnhag",
    "businessname": "Mensa FKSZ",
    "address": "Kreuzbühlstrasse 16, 8008 Zürich"
  }
  JSON
  ```

- [ ] `n-BWhLnW_CQoV6fyxsJARg` — dieci Pizza Kurier Zürich Binz-Wollishofen — Eibenstrasse 24, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "n-BWhLnW_CQoV6fyxsJARg",
    "businessname": "dieci Pizza Kurier Zürich Binz-Wollishofen",
    "address": "Eibenstrasse 24, 8045 Zürich"
  }
  JSON
  ```

- [ ] `vKHyOsZVcOzqXylQ7PFF7A` — Thai Bamboo — Schoffelgasse 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vKHyOsZVcOzqXylQ7PFF7A",
    "businessname": "Thai Bamboo",
    "address": "Schoffelgasse 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `osIeBEOiSevcEDyeAlLIFQ` — Burgermeister Langstrasse — Langstrasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "osIeBEOiSevcEDyeAlLIFQ",
    "businessname": "Burgermeister Langstrasse",
    "address": "Langstrasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `NYlhWa4I2DK8AT6bEtMV4g` — Läckerli Huus AG — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "NYlhWa4I2DK8AT6bEtMV4g",
    "businessname": "Läckerli Huus AG",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `te9dFV16QamBhIXPXnWfpw` — YUMA Restaurant & Bar — Badenerstrasse 120, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "te9dFV16QamBhIXPXnWfpw",
    "businessname": "YUMA Restaurant & Bar",
    "address": "Badenerstrasse 120, 8004 Zürich"
  }
  JSON
  ```

- [ ] `jsFh4ufxNiSMGa4mX8oPmw` — Walliser Keller SwissAlpeChuchi — Zähringerstrasse 21, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jsFh4ufxNiSMGa4mX8oPmw",
    "businessname": "Walliser Keller SwissAlpeChuchi",
    "address": "Zähringerstrasse 21, 8001 Zürich"
  }
  JSON
  ```

- [ ] `XD2xhjEQmCba3XR30tmipQ` — Ba Ba Lu Bar — Schmidgasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XD2xhjEQmCba3XR30tmipQ",
    "businessname": "Ba Ba Lu Bar",
    "address": "Schmidgasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `JsOw-LT4kP0k8plOeca1pw` — Ebrietas Bar — Zähringerstrasse 39, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JsOw-LT4kP0k8plOeca1pw",
    "businessname": "Ebrietas Bar",
    "address": "Zähringerstrasse 39, 8001 Zürich"
  }
  JSON
  ```

- [ ] `x_7yL2O-RL7GcKnzI-V4sw` — At Chuck's — 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "x_7yL2O-RL7GcKnzI-V4sw",
    "businessname": "At Chuck's",
    "address": "8048 Zürich"
  }
  JSON
  ```

- [ ] `DwyKKdsjbKPnbKrQjA1P1g` — my Mythos GmbH — Stauffacherstrasse 35, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DwyKKdsjbKPnbKrQjA1P1g",
    "businessname": "my Mythos GmbH",
    "address": "Stauffacherstrasse 35, 8004 Zürich"
  }
  JSON
  ```

- [ ] `ly_q0RuZR_iPtOdrfzrV9w` — HITZBERGER Sihlcity — Kalanderplatz 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ly_q0RuZR_iPtOdrfzrV9w",
    "businessname": "HITZBERGER Sihlcity",
    "address": "Kalanderplatz 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `quUEW99eCCv5ygpLN6CsRQ` — Bar Rossi — Sihlhallenstrasse 3, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "quUEW99eCCv5ygpLN6CsRQ",
    "businessname": "Bar Rossi",
    "address": "Sihlhallenstrasse 3, 8004 Zürich"
  }
  JSON
  ```

- [ ] `zqBCu2WR7sJXy0QWbC3s9w` — Franzos — Limmatquai 138, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zqBCu2WR7sJXy0QWbC3s9w",
    "businessname": "Franzos",
    "address": "Limmatquai 138, 8001 Zürich"
  }
  JSON
  ```

- [ ] `lL_2RmLqlpfBDhlWd9M5wA` — Pao Pao - Modern Tea - Zurich — Badenerstrasse 156, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lL_2RmLqlpfBDhlWd9M5wA",
    "businessname": "Pao Pao - Modern Tea - Zurich",
    "address": "Badenerstrasse 156, 8004 Zürich"
  }
  JSON
  ```

- [ ] `0ah5c5W6mhJoUfKy4dH04A` — Asia Sytyle Cooking — Langstrasse 117, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0ah5c5W6mhJoUfKy4dH04A",
    "businessname": "Asia Sytyle Cooking",
    "address": "Langstrasse 117, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nVESaL0TOav64BpX8B1Ncg` — CUPCAKE AFFAIR GmbH — Spitalgasse 10, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nVESaL0TOav64BpX8B1Ncg",
    "businessname": "CUPCAKE AFFAIR GmbH",
    "address": "Spitalgasse 10, 8001 Zürich"
  }
  JSON
  ```

- [ ] `y7G0HQ3fJp4yzQxx2xQFJA` — Robin's little Italy — Zähringerstrasse 33, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "y7G0HQ3fJp4yzQxx2xQFJA",
    "businessname": "Robin's little Italy",
    "address": "Zähringerstrasse 33, 8001 Zürich"
  }
  JSON
  ```

- [ ] `vpxonT5CI2Z6Y72pkHEwdw` — Store Kreuzplatz — Kreuzplatz 22, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vpxonT5CI2Z6Y72pkHEwdw",
    "businessname": "Store Kreuzplatz",
    "address": "Kreuzplatz 22, 8008 Zürich"
  }
  JSON
  ```

- [ ] `JSJ8Yb1R5RDzEzvMm03GPg` — Sc hwarzes Schaf - Bistrolino & Bar — Langstrasse 10, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JSJ8Yb1R5RDzEzvMm03GPg",
    "businessname": "Sc hwarzes Schaf - Bistrolino & Bar",
    "address": "Langstrasse 10, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Vwa7lj1C5rqDqBC-0fvkXA` — Lele — Militärstrasse 76, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Vwa7lj1C5rqDqBC-0fvkXA",
    "businessname": "Lele",
    "address": "Militärstrasse 76, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nKWotM1QFLuabeJKWpl1Jg` — Restaurant Schwamedinge — Schwamendingerplatz 2, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nKWotM1QFLuabeJKWpl1Jg",
    "businessname": "Restaurant Schwamedinge",
    "address": "Schwamendingerplatz 2, 8051 Zürich"
  }
  JSON
  ```

- [ ] `YenYf0HF1NebzWXSu1TFAA` — Jane Fine Food — Erlachstrasse 46, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "YenYf0HF1NebzWXSu1TFAA",
    "businessname": "Jane Fine Food",
    "address": "Erlachstrasse 46, 8003 Zürich"
  }
  JSON
  ```

- [ ] `xOsLr9V4nJXwYZCvLxZHdw` — Restaurant Ach'i — Brauerstrasse 4, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xOsLr9V4nJXwYZCvLxZHdw",
    "businessname": "Restaurant Ach'i",
    "address": "Brauerstrasse 4, 8004 Zürich"
  }
  JSON
  ```

- [ ] `ptGCSifyDLkpIn1C426FQQ` — Fondue Stübli — Rotwandstrasse 38, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ptGCSifyDLkpIn1C426FQQ",
    "businessname": "Fondue Stübli",
    "address": "Rotwandstrasse 38, 8004 Zürich"
  }
  JSON
  ```

- [ ] `gVi9nsRXjubk0M8YvadEuw` — Wolf Bierhalle — Limmatquai 132, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gVi9nsRXjubk0M8YvadEuw",
    "businessname": "Wolf Bierhalle",
    "address": "Limmatquai 132, 8001 Zürich"
  }
  JSON
  ```

- [ ] `rKBL-eeub7s-hQbo1uPn1g` — Ristorante Frascati — Bellerivestrasse 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rKBL-eeub7s-hQbo1uPn1g",
    "businessname": "Ristorante Frascati",
    "address": "Bellerivestrasse 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `GTZqSP47NlEajt0NtuLmtQ` — Pizzeria Ristorante Molino Select — Limmatquai 16, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GTZqSP47NlEajt0NtuLmtQ",
    "businessname": "Pizzeria Ristorante Molino Select",
    "address": "Limmatquai 16, 8001 Zürich"
  }
  JSON
  ```

- [ ] `5ZtWvQUJfeYRyJIxI2e0Hg` — Restaurant zum Grünen Glas — Untere Zäune 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5ZtWvQUJfeYRyJIxI2e0Hg",
    "businessname": "Restaurant zum Grünen Glas",
    "address": "Untere Zäune 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `qsF3Cyix_a_EOylY1j9icQ` — Bürgli — Kilchbergstrasse 15, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qsF3Cyix_a_EOylY1j9icQ",
    "businessname": "Bürgli",
    "address": "Kilchbergstrasse 15, 8038 Zürich"
  }
  JSON
  ```

- [ ] `cAJ9muHxJGSr4f6aW-Truw` — Bederhof — Brandschenkestrasse 177, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cAJ9muHxJGSr4f6aW-Truw",
    "businessname": "Bederhof",
    "address": "Brandschenkestrasse 177, 8002 Zürich"
  }
  JSON
  ```

- [ ] `o1IwZprMCdQQpokP647lhA` — Schönau Bar Restaurant — Hohlstrasse 78, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "o1IwZprMCdQQpokP647lhA",
    "businessname": "Schönau Bar Restaurant",
    "address": "Hohlstrasse 78, 8004 Zürich"
  }
  JSON
  ```

- [ ] `mjskVeQsruz29R02aVBaGg` — GAINSBOURG — Kreuzstrasse 26, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "mjskVeQsruz29R02aVBaGg",
    "businessname": "GAINSBOURG",
    "address": "Kreuzstrasse 26, 8008 Zürich"
  }
  JSON
  ```

- [ ] `9Fyly1sg3P6HpFLlGzcRvw` — Lake Side — Bellerivestrasse 170, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "9Fyly1sg3P6HpFLlGzcRvw",
    "businessname": "Lake Side",
    "address": "Bellerivestrasse 170, 8008 Zürich"
  }
  JSON
  ```

- [ ] `ku9KKCl3NEfLVpf306MjXA` — Bar Corazon — Zähringerplatz 11, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ku9KKCl3NEfLVpf306MjXA",
    "businessname": "Bar Corazon",
    "address": "Zähringerplatz 11, 8001 Zürich"
  }
  JSON
  ```

- [ ] `K6WSfUizFBN2FrHIQQgrbQ` — Yokita - japanisches Take Away — Friesenbergstrasse 3, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "K6WSfUizFBN2FrHIQQgrbQ",
    "businessname": "Yokita - japanisches Take Away",
    "address": "Friesenbergstrasse 3, 8055 Zürich"
  }
  JSON
  ```

- [ ] `z2qh3FrdtSZI5VnjlmBKRQ` — The Traders — Leutschenbachstrasse 95, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "z2qh3FrdtSZI5VnjlmBKRQ",
    "businessname": "The Traders",
    "address": "Leutschenbachstrasse 95, 8050 Zürich"
  }
  JSON
  ```

- [ ] `uhUFK0loY8ASCg7Ww3yFkg` — Treff Restaurant-Bar — 8046 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "uhUFK0loY8ASCg7Ww3yFkg",
    "businessname": "Treff Restaurant-Bar",
    "address": "8046 Zürich"
  }
  JSON
  ```

- [ ] `1nZN_KapCRmVs9ZnFWeFbw` — Bridge — Europaallee 22, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "1nZN_KapCRmVs9ZnFWeFbw",
    "businessname": "Bridge",
    "address": "Europaallee 22, 8004 Zürich"
  }
  JSON
  ```

- [ ] `vR4bMDntsWEMepv6hKphCA` — Starbucks — Limmatquai 4, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vR4bMDntsWEMepv6hKphCA",
    "businessname": "Starbucks",
    "address": "Limmatquai 4, 8001 Zürich"
  }
  JSON
  ```

- [ ] `U6ip9Je5RmaR5_Zl0-Mwfw` — Gran Café Motta — Limmatquai 66, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "U6ip9Je5RmaR5_Zl0-Mwfw",
    "businessname": "Gran Café Motta",
    "address": "Limmatquai 66, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Iawvt6K4UYoWzw1DQnWW1Q` — Regenbogen Bar — Rosengasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Iawvt6K4UYoWzw1DQnWW1Q",
    "businessname": "Regenbogen Bar",
    "address": "Rosengasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `2WBGVDPb-t0L3DXEbmEUmg` — Königstuhl Gastronomie AG — Stüssihofstatt 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2WBGVDPb-t0L3DXEbmEUmg",
    "businessname": "Königstuhl Gastronomie AG",
    "address": "Stüssihofstatt 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `E4PRpGB_XvKldBB997onCA` — Zeder — Badenerstrasse 78, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "E4PRpGB_XvKldBB997onCA",
    "businessname": "Zeder",
    "address": "Badenerstrasse 78, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Odpfu2gF063riEgLb0RUzg` — Robin's Coffee — Zähringerstrasse 33, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Odpfu2gF063riEgLb0RUzg",
    "businessname": "Robin's Coffee",
    "address": "Zähringerstrasse 33, 8001 Zürich"
  }
  JSON
  ```

- [ ] `PYqicaf3HuGpW86SXvPnIg` — Blue Monkey - Authentic Thai Restaurant — Stüssihofstatt 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "PYqicaf3HuGpW86SXvPnIg",
    "businessname": "Blue Monkey - Authentic Thai Restaurant",
    "address": "Stüssihofstatt 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `rOk4JftiGIaruIOBrEl0gg` — Vesuvio Pizzeria Da Antonio — Glatttalstrasse 40, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rOk4JftiGIaruIOBrEl0gg",
    "businessname": "Vesuvio Pizzeria Da Antonio",
    "address": "Glatttalstrasse 40, 8052 Zürich"
  }
  JSON
  ```

- [ ] `LMS3oC1ON2AhRdbFXmKflQ` — China Restaurant Chop-Stick — Niederdorfstrasse 82, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "LMS3oC1ON2AhRdbFXmKflQ",
    "businessname": "China Restaurant Chop-Stick",
    "address": "Niederdorfstrasse 82, 8001 Zürich"
  }
  JSON
  ```

- [ ] `bf6de36tXC_KcjYCN17b1A` — Schnupf — Neufrankengasse 29, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "bf6de36tXC_KcjYCN17b1A",
    "businessname": "Schnupf",
    "address": "Neufrankengasse 29, 8004 Zürich"
  }
  JSON
  ```

- [ ] `auswhz3dG0isYjZXyuFwLg` — Ristorante La Pasta AG — Niederdorfstrasse 80, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "auswhz3dG0isYjZXyuFwLg",
    "businessname": "Ristorante La Pasta AG",
    "address": "Niederdorfstrasse 80, 8001 Zürich"
  }
  JSON
  ```

- [ ] `p070TsdEjhstjgkDZb3R3w` — Winter Garte Europaallee Zürich — Gustav-Gull-Platz, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "p070TsdEjhstjgkDZb3R3w",
    "businessname": "Winter Garte Europaallee Zürich",
    "address": "Gustav-Gull-Platz, 8004 Zürich"
  }
  JSON
  ```

- [ ] `SDTb-wE1gBaeBXuSCv3qZw` — Ristorante Pizzeria Don Emilio — Dübendorfstrasse 24, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "SDTb-wE1gBaeBXuSCv3qZw",
    "businessname": "Ristorante Pizzeria Don Emilio",
    "address": "Dübendorfstrasse 24, 8051 Zürich"
  }
  JSON
  ```

- [ ] `RZEpT4XvanBRSghcba7B_g` — FELFEL AG — Grubenstrasse 11, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RZEpT4XvanBRSghcba7B_g",
    "businessname": "FELFEL AG",
    "address": "Grubenstrasse 11, 8045 Zürich"
  }
  JSON
  ```

- [ ] `sl3WAKssnNCNWVNclYLybA` — Kantorei — Spiegelgasse 33, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sl3WAKssnNCNWVNclYLybA",
    "businessname": "Kantorei",
    "address": "Spiegelgasse 33, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Xkqvx2F1J3k4Mkd60p-RyA` — Restaurant Ländli Züri — Feldeggstrasse 87, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Xkqvx2F1J3k4Mkd60p-RyA",
    "businessname": "Restaurant Ländli Züri",
    "address": "Feldeggstrasse 87, 8008 Zürich"
  }
  JSON
  ```

- [ ] `NIQfc90KxOjHIrNDGS5wAQ` — John Baker Helvetia Ltd. — Molkenstrasse 15, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "NIQfc90KxOjHIrNDGS5wAQ",
    "businessname": "John Baker Helvetia Ltd.",
    "address": "Molkenstrasse 15, 8004 Zürich"
  }
  JSON
  ```

- [ ] `FZ8apve1S3xjkVynGTRAqA` — Imbiss Riviera — Utoquai 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FZ8apve1S3xjkVynGTRAqA",
    "businessname": "Imbiss Riviera",
    "address": "Utoquai 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `hGpFjfj4qdifNKWeTT5ZDg` — Vasco's Bar — Bäckerstrasse 20, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "hGpFjfj4qdifNKWeTT5ZDg",
    "businessname": "Vasco's Bar",
    "address": "Bäckerstrasse 20, 8004 Zürich"
  }
  JSON
  ```

- [ ] `iYYBBw4rzOyifDU1EdBsHQ` — Hotel Hirschen — Niederdorfstrasse 13, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "iYYBBw4rzOyifDU1EdBsHQ",
    "businessname": "Hotel Hirschen",
    "address": "Niederdorfstrasse 13, 8001 Zürich"
  }
  JSON
  ```

- [ ] `8MZgnVV2l6sORbzD8bMgyQ` — Ristorante Più Europaallee — Kasernenstrasse 95, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8MZgnVV2l6sORbzD8bMgyQ",
    "businessname": "Ristorante Più Europaallee",
    "address": "Kasernenstrasse 95, 8004 Zürich"
  }
  JSON
  ```

- [ ] `FRM8rwp_-V8gO6Ko6GChRw` — Restaurant Volkshaus — Stauffacherstrasse 60, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FRM8rwp_-V8gO6Ko6GChRw",
    "businessname": "Restaurant Volkshaus",
    "address": "Stauffacherstrasse 60, 8004 Zürich"
  }
  JSON
  ```

- [ ] `6b6_4CXIyn9J94yKDxCDeQ` — Filini Restaurant — Postfach 295, 8058 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6b6_4CXIyn9J94yKDxCDeQ",
    "businessname": "Filini Restaurant",
    "address": "Postfach 295, 8058 Zürich"
  }
  JSON
  ```

- [ ] `--4_mVtsTB60xycsWAE6EA` — Cristina Test — Berninaplatz 2, 8057 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "--4_mVtsTB60xycsWAE6EA",
    "businessname": "Cristina Test",
    "address": "Berninaplatz 2, 8057 Zürich"
  }
  JSON
  ```

- [ ] `T3x8IL6LrMteVrw2sK8jlA` — Thai Bogie Kitchen — Neunbrunnenstrasse 50, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "T3x8IL6LrMteVrw2sK8jlA",
    "businessname": "Thai Bogie Kitchen",
    "address": "Neunbrunnenstrasse 50, 8050 Zürich"
  }
  JSON
  ```

- [ ] `87kgOtDY0eEUa6-JEGmb7w` — Smeily's — Bernistrasse 43  Oerlikon, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "87kgOtDY0eEUa6-JEGmb7w",
    "businessname": "Smeily's",
    "address": "Bernistrasse 43  Oerlikon, 8057 Zürich"
  }
  JSON
  ```

- [ ] `oFCqW_DvzGXc0sRxfdXi9g` — Träffpunkt — Regensbergstrasse 188, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "oFCqW_DvzGXc0sRxfdXi9g",
    "businessname": "Träffpunkt",
    "address": "Regensbergstrasse 188, 8050 Zürich"
  }
  JSON
  ```

- [ ] `HZf9fYnhQMCAZMCj1Yib-A` — Restaurant Neue Taverne — Glockengasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HZf9fYnhQMCAZMCj1Yib-A",
    "businessname": "Restaurant Neue Taverne",
    "address": "Glockengasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `tu7sKw7PQYEEvawwWlBOZA` — Panama Bar - Grill — Lettensteg 10, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "tu7sKw7PQYEEvawwWlBOZA",
    "businessname": "Panama Bar - Grill",
    "address": "Lettensteg 10, 8037 Zürich"
  }
  JSON
  ```

- [ ] `EoCNsf-7k8Mv1siijeSrBQ` — Nüni — Hohlstrasse 430, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EoCNsf-7k8Mv1siijeSrBQ",
    "businessname": "Nüni",
    "address": "Hohlstrasse 430, 8048 Zürich"
  }
  JSON
  ```

- [ ] `IEpVYSQs2fJHefRLIGgUqw` — Café & Beck Oberstrass — Universitätstrasse 9, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IEpVYSQs2fJHefRLIGgUqw",
    "businessname": "Café & Beck Oberstrass",
    "address": "Universitätstrasse 9, 8006 Zürich"
  }
  JSON
  ```

- [ ] `JZ9BgkElQFwF3V8os1aXug` — Maki Haus Inh. Yao — Stampfenbachstrasse 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JZ9BgkElQFwF3V8os1aXug",
    "businessname": "Maki Haus Inh. Yao",
    "address": "Stampfenbachstrasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `DolGkCh_RxQ9nAsBq90i9w` — Steakhaus & Pizzeria Mattenhof — Dübendorfstrasse 321, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DolGkCh_RxQ9nAsBq90i9w",
    "businessname": "Steakhaus & Pizzeria Mattenhof",
    "address": "Dübendorfstrasse 321, 8051 Zürich"
  }
  JSON
  ```

- [ ] `Wzmdaon4fatknoNRbxW_Gw` — Alters - und Pflegezentrum Herrenbergli, Zürich-Altstetten — Am Suteracher 65, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Wzmdaon4fatknoNRbxW_Gw",
    "businessname": "Alters - und Pflegezentrum Herrenbergli, Zürich-Altstetten",
    "address": "Am Suteracher 65, 8048 Zürich"
  }
  JSON
  ```

- [ ] `mYoSNlOLmcgOfqd1_0nihw` — Lenox Bar — Neumühlequai 42, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "mYoSNlOLmcgOfqd1_0nihw",
    "businessname": "Lenox Bar",
    "address": "Neumühlequai 42, 8006 Zürich"
  }
  JSON
  ```

- [ ] `nXK1lySWOQE8-uT9HbHdoQ` — Anoah - Plant Based — Rigiplatz 1, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nXK1lySWOQE8-uT9HbHdoQ",
    "businessname": "Anoah - Plant Based",
    "address": "Rigiplatz 1, 8006 Zürich"
  }
  JSON
  ```

- [ ] `ZbsOxmjAvUqvzXR5YXi2bw` — S. Ip's Pub — Schaffhauserstrasse 380, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZbsOxmjAvUqvzXR5YXi2bw",
    "businessname": "S. Ip's Pub",
    "address": "Schaffhauserstrasse 380, 8050 Zürich"
  }
  JSON
  ```

- [ ] `wxLajjkJUmDuSHiZPBQ5nA` — Restaurant Bernadette — Sechseläutenplatz 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "wxLajjkJUmDuSHiZPBQ5nA",
    "businessname": "Restaurant Bernadette",
    "address": "Sechseläutenplatz 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `7OqrJZsSMgO4GInyDOd_SQ` — Restaurant Spitz — Museumstrasse 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7OqrJZsSMgO4GInyDOd_SQ",
    "businessname": "Restaurant Spitz",
    "address": "Museumstrasse 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `F_oqZH7lhMCRwXjiHweuVg` — Dr. Zhivago AG — Bärengasse 29, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "F_oqZH7lhMCRwXjiHweuVg",
    "businessname": "Dr. Zhivago AG",
    "address": "Bärengasse 29, 8001 Zürich"
  }
  JSON
  ```

- [ ] `QFF-4OC5HNrhsBLMMglHyQ` — Züri Burg — Badenerstrasse 659, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "QFF-4OC5HNrhsBLMMglHyQ",
    "businessname": "Züri Burg",
    "address": "Badenerstrasse 659, 8048 Zürich"
  }
  JSON
  ```

- [ ] `Ah-38M1XR1AJK0dlizBJjw` — Restaurant Münsterhof — Münsterhof 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Ah-38M1XR1AJK0dlizBJjw",
    "businessname": "Restaurant Münsterhof",
    "address": "Münsterhof 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `j8B4XwZOUom2bQtzx14NgQ` — Josef — Gasometerstrasse 24, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "j8B4XwZOUom2bQtzx14NgQ",
    "businessname": "Josef",
    "address": "Gasometerstrasse 24, 8005 Zürich"
  }
  JSON
  ```

- [ ] `sSeFvTUgntRAd0r7xoDidw` — Yooji's Passage Sihlquai — Museumstrasse 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sSeFvTUgntRAd0r7xoDidw",
    "businessname": "Yooji's Passage Sihlquai",
    "address": "Museumstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `GWKVgM6vlrhQgXEEzLJpnw` — Haute SA — Talstrasse 65, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GWKVgM6vlrhQgXEEzLJpnw",
    "businessname": "Haute SA",
    "address": "Talstrasse 65, 8001 Zürich"
  }
  JSON
  ```

- [ ] `wt-SrDdz5QsPWAjVhePLUA` — SAM'S Pizza Land — Schweizergasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "wt-SrDdz5QsPWAjVhePLUA",
    "businessname": "SAM'S Pizza Land",
    "address": "Schweizergasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `4JM7Qimpdip5SgwMHEXgTA` — Chaima Thai Take Away GmbH — Lägernstrasse 32, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4JM7Qimpdip5SgwMHEXgTA",
    "businessname": "Chaima Thai Take Away GmbH",
    "address": "Lägernstrasse 32, 8037 Zürich"
  }
  JSON
  ```

- [ ] `YQGL32WHaEnI6Q-xIru08A` — Imagine — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "YQGL32WHaEnI6Q-xIru08A",
    "businessname": "Imagine",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `esPyDxYOEJYF6AEohcB5HA` — Lumière AG — Widdergasse 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "esPyDxYOEJYF6AEohcB5HA",
    "businessname": "Lumière AG",
    "address": "Widdergasse 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `sfr1guUd5BFWUEPvRs03Gg` — Musti Grill — Saumackerstrasse 48, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sfr1guUd5BFWUEPvRs03Gg",
    "businessname": "Musti Grill",
    "address": "Saumackerstrasse 48, 8048 Zürich"
  }
  JSON
  ```

- [ ] `rBItADCQPzNsvCVrwYdWtw` — Restaurant Burgwies — Forchstrasse 271, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rBItADCQPzNsvCVrwYdWtw",
    "businessname": "Restaurant Burgwies",
    "address": "Forchstrasse 271, 8008 Zürich"
  }
  JSON
  ```

- [ ] `NU-rSFZW6o1iJ20pABoSHA` — Cheyenne — Querstrasse 3, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "NU-rSFZW6o1iJ20pABoSHA",
    "businessname": "Cheyenne",
    "address": "Querstrasse 3, 8050 Zürich"
  }
  JSON
  ```

- [ ] `W91yhXn3A7SsRr4_1MTqaA` — Ellermann 's Hummerbar — Bahnhofstrasse 87, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "W91yhXn3A7SsRr4_1MTqaA",
    "businessname": "Ellermann 's Hummerbar",
    "address": "Bahnhofstrasse 87, 8001 Zürich"
  }
  JSON
  ```

- [ ] `E2FE14_t_A8FFW9_xUkXBQ` — George Bar & Grill — Gessnerallee 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "E2FE14_t_A8FFW9_xUkXBQ",
    "businessname": "George Bar & Grill",
    "address": "Gessnerallee 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `4judvzzAu37tGMZ2JoEz8Q` — Curry Queen — Badenerstrasse 663, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4judvzzAu37tGMZ2JoEz8Q",
    "businessname": "Curry Queen",
    "address": "Badenerstrasse 663, 8048 Zürich"
  }
  JSON
  ```

- [ ] `rq5Bkt5YgsPIaoycH0YwlA` — Churrasco Steak & Nikkei Cuisine — Glockengasse 9, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rq5Bkt5YgsPIaoycH0YwlA",
    "businessname": "Churrasco Steak & Nikkei Cuisine",
    "address": "Glockengasse 9, 8001 Zürich"
  }
  JSON
  ```

- [ ] `3puXcuzInvHY75hC5YU6AQ` — Il Pentagramma — Josefstrasse 28, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3puXcuzInvHY75hC5YU6AQ",
    "businessname": "Il Pentagramma",
    "address": "Josefstrasse 28, 8005 Zürich"
  }
  JSON
  ```

- [ ] `f8mBzVzuliu3x8uMUOR11Q` — Sprössling — Hotzestrasse 65, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "f8mBzVzuliu3x8uMUOR11Q",
    "businessname": "Sprössling",
    "address": "Hotzestrasse 65, 8006 Zürich"
  }
  JSON
  ```

- [ ] `Xj44swhjOqEaXWEnW9CT7A` — Parea — Zentralstrasse 161, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Xj44swhjOqEaXWEnW9CT7A",
    "businessname": "Parea",
    "address": "Zentralstrasse 161, 8003 Zürich"
  }
  JSON
  ```

- [ ] `kgcY-7Brw-cIuOBIJjGv9Q` — VAPIANO — Rämistrasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kgcY-7Brw-cIuOBIJjGv9Q",
    "businessname": "VAPIANO",
    "address": "Rämistrasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HwTkY_u1CXxCT7gdnMCOAg` — Lotti Restaurant Bar Cafe Grill — Werdmühleplatz 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HwTkY_u1CXxCT7gdnMCOAg",
    "businessname": "Lotti Restaurant Bar Cafe Grill",
    "address": "Werdmühleplatz 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `bOnLwqK2IMVUHPihMwa8bQ` — Casino Restaurant — Badenerstrasse 647, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "bOnLwqK2IMVUHPihMwa8bQ",
    "businessname": "Casino Restaurant",
    "address": "Badenerstrasse 647, 8048 Zürich"
  }
  JSON
  ```

- [ ] `pGBZL2dxHT1UDfWHKFWKBA` — Restaurant Thai Erawan — Badenerstrasse 811, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pGBZL2dxHT1UDfWHKFWKBA",
    "businessname": "Restaurant Thai Erawan",
    "address": "Badenerstrasse 811, 8048 Zürich"
  }
  JSON
  ```

- [ ] `jhOjJPylVqidkQRcSuEAtA` — Zunfthaus zum Widder — Rennweg 7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jhOjJPylVqidkQRcSuEAtA",
    "businessname": "Zunfthaus zum Widder",
    "address": "Rennweg 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `-JvxPXQf4cuchLqjsZzX5A` — McDonald's — Gottfried-Keller-Strasse 7, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-JvxPXQf4cuchLqjsZzX5A",
    "businessname": "McDonald's",
    "address": "Gottfried-Keller-Strasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `zVDz9IOruY5UszDAf36TwQ` — Restaurant Oval — Badenerstrasse 500, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zVDz9IOruY5UszDAf36TwQ",
    "businessname": "Restaurant Oval",
    "address": "Badenerstrasse 500, 8048 Zürich"
  }
  JSON
  ```

- [ ] `Yb_rYkJF2m1xVbpJeHz-fA` — Restaurant Hato — Brandschenkestrasse 20, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Yb_rYkJF2m1xVbpJeHz-fA",
    "businessname": "Restaurant Hato",
    "address": "Brandschenkestrasse 20, 8001 Zürich"
  }
  JSON
  ```

- [ ] `ZuM_2ihNQSp5gVoqFeay2Q` — Namamen — Vulkanplatz 9, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZuM_2ihNQSp5gVoqFeay2Q",
    "businessname": "Namamen",
    "address": "Vulkanplatz 9, 8048 Zürich"
  }
  JSON
  ```

- [ ] `oMVxcBGUH4IgpHzBhgL4rg` — Zurich Fine Chocolate and Cake — Waserstrasse 76, 8053 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "oMVxcBGUH4IgpHzBhgL4rg",
    "businessname": "Zurich Fine Chocolate and Cake",
    "address": "Waserstrasse 76, 8053 Zürich"
  }
  JSON
  ```

- [ ] `50Q67kcmvE_FPE-zx9zkvg` — MyLOCALINA Free Showcase (FR) — Förrlibuckstrasse 62, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "50Q67kcmvE_FPE-zx9zkvg",
    "businessname": "MyLOCALINA Free Showcase (FR)",
    "address": "Förrlibuckstrasse 62, 8005 Zürich"
  }
  JSON
  ```

- [ ] `xi32XFsUAWwpbUKCsnxkcA` — Restaurant Vulkan — Klingenstrasse 33, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xi32XFsUAWwpbUKCsnxkcA",
    "businessname": "Restaurant Vulkan",
    "address": "Klingenstrasse 33, 8005 Zürich"
  }
  JSON
  ```

- [ ] `js1V8FX4imLlcxRUoNAkXg` — YUKA - Restau rant & Bar — Stampfenbachstrasse 60, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "js1V8FX4imLlcxRUoNAkXg",
    "businessname": "YUKA - Restau rant & Bar",
    "address": "Stampfenbachstrasse 60, 8006 Zürich"
  }
  JSON
  ```

- [ ] `4Y7v1IpAubUxGlr3yTHikg` — Il Punto — Zschokkestrasse 1, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4Y7v1IpAubUxGlr3yTHikg",
    "businessname": "Il Punto",
    "address": "Zschokkestrasse 1, 8037 Zürich"
  }
  JSON
  ```

- [ ] `XlOM3DSqSoeHWjGtRZozEw` — Haus Hiltl — Sihlstrasse 28, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XlOM3DSqSoeHWjGtRZozEw",
    "businessname": "Haus Hiltl",
    "address": "Sihlstrasse 28, 8001 Zürich"
  }
  JSON
  ```

- [ ] `8XAemi_ipOq-UdiIfJI8Pw` — Restaurant R21 — Orellistrasse 21, 8044 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8XAemi_ipOq-UdiIfJI8Pw",
    "businessname": "Restaurant R21",
    "address": "Orellistrasse 21, 8044 Zürich"
  }
  JSON
  ```

- [ ] `eDDH6OTlSl9qcj3_7kNWPQ` — SBB Restaurant Oase — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "eDDH6OTlSl9qcj3_7kNWPQ",
    "businessname": "SBB Restaurant Oase",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `1um85w1y9hhMWOSujXYfcw` — Restaurant Pavillon — Talstrasse 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "1um85w1y9hhMWOSujXYfcw",
    "businessname": "Restaurant Pavillon",
    "address": "Talstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `76FPInMVFXpDvaGYztXSBA` — Lobby — Bahnhofstrasse 87, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "76FPInMVFXpDvaGYztXSBA",
    "businessname": "Lobby",
    "address": "Bahnhofstrasse 87, 8001 Zürich"
  }
  JSON
  ```

- [ ] `4gxowGVKbgS7l26PTmAgtQ` — Jules Verne Panoramabar — Uraniastrasse 9, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4gxowGVKbgS7l26PTmAgtQ",
    "businessname": "Jules Verne Panoramabar",
    "address": "Uraniastrasse 9, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CG8bQYi4A9UG4GPtacqqgA` — Schmiedhof Alters- und Pflegeheim — Zweierstrasse 138, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CG8bQYi4A9UG4GPtacqqgA",
    "businessname": "Schmiedhof Alters- und Pflegeheim",
    "address": "Zweierstrasse 138, 8003 Zürich"
  }
  JSON
  ```

- [ ] `53M1g1dEJqqVQ2TAqBCDkg` — Friends Corner — Josefstrasse 146, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "53M1g1dEJqqVQ2TAqBCDkg",
    "businessname": "Friends Corner",
    "address": "Josefstrasse 146, 8005 Zürich"
  }
  JSON
  ```

- [ ] `P3husr1GCG6i7yvdUNGn4w` — Aroma — Asylstrasse 110, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "P3husr1GCG6i7yvdUNGn4w",
    "businessname": "Aroma",
    "address": "Asylstrasse 110, 8032 Zürich"
  }
  JSON
  ```

- [ ] `0TsjbrVp93g0B2_2yXFrUw` — 4. Akt — Heinrichstrasse 262, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0TsjbrVp93g0B2_2yXFrUw",
    "businessname": "4. Akt",
    "address": "Heinrichstrasse 262, 8005 Zürich"
  }
  JSON
  ```

- [ ] `pv-x3LBNbYUmWtBr7gbirw` — Tapas & Friends — Aemtlerstrasse 86, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pv-x3LBNbYUmWtBr7gbirw",
    "businessname": "Tapas & Friends",
    "address": "Aemtlerstrasse 86, 8003 Zürich"
  }
  JSON
  ```

- [ ] `W-Zay401NcMFZeIDx4kavA` — Store Stadelhofen — Theaterstrasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "W-Zay401NcMFZeIDx4kavA",
    "businessname": "Store Stadelhofen",
    "address": "Theaterstrasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Fg3lUB0JB1cS4SkENIKHVg` — Jamaican Flavour — Langstrasse 200, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Fg3lUB0JB1cS4SkENIKHVg",
    "businessname": "Jamaican Flavour",
    "address": "Langstrasse 200, 8005 Zürich"
  }
  JSON
  ```

- [ ] `xPNMLk1ZleTNjeIW8ierjw` — Gelateria Di Berna — Weststrasse 196, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xPNMLk1ZleTNjeIW8ierjw",
    "businessname": "Gelateria Di Berna",
    "address": "Weststrasse 196, 8003 Zürich"
  }
  JSON
  ```

- [ ] `Nmy6we8IHBZrleNrzhuDAQ` — Zoocafé — Zürichbergstrasse 219, 8044 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Nmy6we8IHBZrleNrzhuDAQ",
    "businessname": "Zoocafé",
    "address": "Zürichbergstrasse 219, 8044 Zürich"
  }
  JSON
  ```

- [ ] `Vp--1CamLPnXEI4Qi-cfrA` — Zur Taverne WeinArt — Imbisbühlstrasse 7, 8049 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Vp--1CamLPnXEI4Qi-cfrA",
    "businessname": "Zur Taverne WeinArt",
    "address": "Imbisbühlstrasse 7, 8049 Zürich"
  }
  JSON
  ```

- [ ] `cAkBYHpHyEhXDTtRO_i_Ow` — dean & david ZH Bleicherweg GmbH — Bleicherweg 19, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cAkBYHpHyEhXDTtRO_i_Ow",
    "businessname": "dean & david ZH Bleicherweg GmbH",
    "address": "Bleicherweg 19, 8002 Zürich"
  }
  JSON
  ```

- [ ] `KSXyJ3WLBMhr3vHCQbuCiA` — Yooji's Josef — Josefstrasse 112, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KSXyJ3WLBMhr3vHCQbuCiA",
    "businessname": "Yooji's Josef",
    "address": "Josefstrasse 112, 8005 Zürich"
  }
  JSON
  ```

- [ ] `IyYTEwOjHz_tdKABndLpkQ` — Panorama Restaurant Albisgütli — Uetlibergstrasse 331, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IyYTEwOjHz_tdKABndLpkQ",
    "businessname": "Panorama Restaurant Albisgütli",
    "address": "Uetlibergstrasse 331, 8045 Zürich"
  }
  JSON
  ```

- [ ] `SPdRx8sTHn0y4od94X-aDA` — Bibim Shack — Hardstrasse 322, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "SPdRx8sTHn0y4od94X-aDA",
    "businessname": "Bibim Shack",
    "address": "Hardstrasse 322, 8005 Zürich"
  }
  JSON
  ```

- [ ] `VcoAdIEPQr0DAFaE3B0p6A` — Margheri — Limmatstrasse 273, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VcoAdIEPQr0DAFaE3B0p6A",
    "businessname": "Margheri",
    "address": "Limmatstrasse 273, 8005 Zürich"
  }
  JSON
  ```

- [ ] `_2GdVCRXmtinI_PDX04Ouw` — il bistrò — Konradstrasse 40, 8005 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_2GdVCRXmtinI_PDX04Ouw",
    "businessname": "il bistrò",
    "address": "Konradstrasse 40, 8005 Zürich"
  }
  JSON
  ```

- [ ] `2NVZ8SS13bUH_eD-c9-60w` — Napi's Thai Restaurant & Take Away — Flurstrasse 4, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2NVZ8SS13bUH_eD-c9-60w",
    "businessname": "Napi's Thai Restaurant & Take Away",
    "address": "Flurstrasse 4, 8048 Zürich"
  }
  JSON
  ```

- [ ] `MycWn5pw2nF5md4WXsNHLg` — Pizzeria Unico — Limmatstrasse 273, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "MycWn5pw2nF5md4WXsNHLg",
    "businessname": "Pizzeria Unico",
    "address": "Limmatstrasse 273, 8005 Zürich"
  }
  JSON
  ```

- [ ] `YSBt7D1CzyB4pQvcTt9RWw` — Sai Somsak — Neue Hard 9, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "YSBt7D1CzyB4pQvcTt9RWw",
    "businessname": "Sai Somsak",
    "address": "Neue Hard 9, 8005 Zürich"
  }
  JSON
  ```

- [ ] `P_QiM7s_0K2UYUMFxTZ61A` — Pause im Foifi — Förrlibuckstrasse 70, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "P_QiM7s_0K2UYUMFxTZ61A",
    "businessname": "Pause im Foifi",
    "address": "Förrlibuckstrasse 70, 8005 Zürich"
  }
  JSON
  ```

- [ ] `z2TJMdR3P13K74Wqq3mDwg` — Martin Puppel Architekt — Dorfstrasse 40, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "z2TJMdR3P13K74Wqq3mDwg",
    "businessname": "Martin Puppel Architekt",
    "address": "Dorfstrasse 40, 8037 Zürich"
  }
  JSON
  ```

- [ ] `LmSQOuVdrCwiiJbikdDDtA` — Bäckerei Hug — Goethestrasse 14, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "LmSQOuVdrCwiiJbikdDDtA",
    "businessname": "Bäckerei Hug",
    "address": "Goethestrasse 14, 8001 Zürich"
  }
  JSON
  ```

- [ ] `M6l7Qg2LxgEKshf-cMiuxQ` — Lily's — Langstrasse 197, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "M6l7Qg2LxgEKshf-cMiuxQ",
    "businessname": "Lily's",
    "address": "Langstrasse 197, 8005 Zürich"
  }
  JSON
  ```

- [ ] `ebL5lpmoGyOe66NPGjymgA` — Al Mouchtar — Hafnerstrasse 13, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ebL5lpmoGyOe66NPGjymgA",
    "businessname": "Al Mouchtar",
    "address": "Hafnerstrasse 13, 8005 Zürich"
  }
  JSON
  ```

- [ ] `zfLN80ZlqkE3bL3XhDuInQ` — Iberico — Milchbuckstrasse 11, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zfLN80ZlqkE3bL3XhDuInQ",
    "businessname": "Iberico",
    "address": "Milchbuckstrasse 11, 8057 Zürich"
  }
  JSON
  ```

- [ ] `1_J7HVsc8xdR0bjh--EBcw` — Alegria Restaurante Peruano — Seestrasse 361, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "1_J7HVsc8xdR0bjh--EBcw",
    "businessname": "Alegria Restaurante Peruano",
    "address": "Seestrasse 361, 8038 Zürich"
  }
  JSON
  ```

- [ ] `7MxE3WGKmZo8yWmqlGLtmw` — 25hours Hotel Zürich West — Pfingstweidstrasse 102, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7MxE3WGKmZo8yWmqlGLtmw",
    "businessname": "25hours Hotel Zürich West",
    "address": "Pfingstweidstrasse 102, 8005 Zürich"
  }
  JSON
  ```

- [ ] `u7n_c4xXz_8PHU25Jghn-Q` — Starbucks Coffee — Winterthurerstrasse 698, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "u7n_c4xXz_8PHU25Jghn-Q",
    "businessname": "Starbucks Coffee",
    "address": "Winterthurerstrasse 698, 8051 Zürich"
  }
  JSON
  ```

- [ ] `W7z76pmwquA3CALe67NzAg` — Route twenty-six — Pfingstweidstrasse 100, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "W7z76pmwquA3CALe67NzAg",
    "businessname": "Route twenty-six",
    "address": "Pfingstweidstrasse 100, 8005 Zürich"
  }
  JSON
  ```

- [ ] `OlEmxhIfqiwo1q4S5XYr_g` — Restaurant Haldenbach — Haldenbachstrasse 2, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OlEmxhIfqiwo1q4S5XYr_g",
    "businessname": "Restaurant Haldenbach",
    "address": "Haldenbachstrasse 2, 8006 Zürich"
  }
  JSON
  ```

- [ ] `TcUB_uVt5dZdkdr7m6YlCA` — Soul St Zurich — Döltschiweg 234, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "TcUB_uVt5dZdkdr7m6YlCA",
    "businessname": "Soul St Zurich",
    "address": "Döltschiweg 234, 8055 Zürich"
  }
  JSON
  ```

- [ ] `V6PwrJ20W-0PGPxBF2o47A` — apoTHEKE Gastro AG — Zürichbergstrasse 17, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "V6PwrJ20W-0PGPxBF2o47A",
    "businessname": "apoTHEKE Gastro AG",
    "address": "Zürichbergstrasse 17, 8032 Zürich"
  }
  JSON
  ```

- [ ] `extXgA1oQCOX8TVdxpJZSw` — Nishi Japan Shop — Schaffhauserstrasse 120, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "extXgA1oQCOX8TVdxpJZSw",
    "businessname": "Nishi Japan Shop",
    "address": "Schaffhauserstrasse 120, 8057 Zürich"
  }
  JSON
  ```

- [ ] `umvLfWqH7j3lVg8jrXrN2Q` — Dune Oriental Lounge Privatclub — Josefstrasse 29, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "umvLfWqH7j3lVg8jrXrN2Q",
    "businessname": "Dune Oriental Lounge Privatclub",
    "address": "Josefstrasse 29, 8005 Zürich"
  }
  JSON
  ```

- [ ] `qnpeRTKRnm2rUQRRHLvx0w` — Restaurant Weisses Rössli — Bederstrasse 96, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qnpeRTKRnm2rUQRRHLvx0w",
    "businessname": "Restaurant Weisses Rössli",
    "address": "Bederstrasse 96, 8002 Zürich"
  }
  JSON
  ```

- [ ] `RBUKNfajQC1y4ies4a2RVg` — Domino's Pizza Zürich Goldbrunnen — Goldbrunnenstrasse 115, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RBUKNfajQC1y4ies4a2RVg",
    "businessname": "Domino's Pizza Zürich Goldbrunnen",
    "address": "Goldbrunnenstrasse 115, 8055 Zürich"
  }
  JSON
  ```

- [ ] `qPQ2u2uUQBxJ8thcccwKDg` — Tremonte Catering GmbH — Birmensdorferstrasse 129, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qPQ2u2uUQBxJ8thcccwKDg",
    "businessname": "Tremonte Catering GmbH",
    "address": "Birmensdorferstrasse 129, 8003 Zürich"
  }
  JSON
  ```

- [ ] `_Jeyw_HbIZVo4H-6Qty-3w` — Costa Brava — Limmatstrasse 267, 8005 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_Jeyw_HbIZVo4H-6Qty-3w",
    "businessname": "Costa Brava",
    "address": "Limmatstrasse 267, 8005 Zürich"
  }
  JSON
  ```

- [ ] `cwoYfOSqISahxaz64nCp6w` — Rosaly's Restaurant & Bar — Freieckgasse 7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cwoYfOSqISahxaz64nCp6w",
    "businessname": "Rosaly's Restaurant & Bar",
    "address": "Freieckgasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gCN7t1vHL33sJTelEPrpsg` — Tillsamman GmbH — Sihlfeldstrasse 10, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gCN7t1vHL33sJTelEPrpsg",
    "businessname": "Tillsamman GmbH",
    "address": "Sihlfeldstrasse 10, 8003 Zürich"
  }
  JSON
  ```

- [ ] `qRfr42BwOKKzeuN9o8fZyQ` — ease DESIGN SPA — Giessereistrasse 18, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qRfr42BwOKKzeuN9o8fZyQ",
    "businessname": "ease DESIGN SPA",
    "address": "Giessereistrasse 18, 8005 Zürich"
  }
  JSON
  ```

- [ ] `bAbSw1KgA_y7ZMcdlHFbSA` — Chop Chop Asian Delight — Josefstrasse 102, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "bAbSw1KgA_y7ZMcdlHFbSA",
    "businessname": "Chop Chop Asian Delight",
    "address": "Josefstrasse 102, 8005 Zürich"
  }
  JSON
  ```

- [ ] `2eFu_KcEvsKwg1R6aYMcOw` — Züri Bistro Milchbuck — Schaffhauserstrasse 126, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2eFu_KcEvsKwg1R6aYMcOw",
    "businessname": "Züri Bistro Milchbuck",
    "address": "Schaffhauserstrasse 126, 8057 Zürich"
  }
  JSON
  ```

- [ ] `AQBT2dbVgNKBbvY8KI93_g` — Sushi Palace — Thurgauerstrasse 23, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AQBT2dbVgNKBbvY8KI93_g",
    "businessname": "Sushi Palace",
    "address": "Thurgauerstrasse 23, 8050 Zürich"
  }
  JSON
  ```

- [ ] `ZehDEfIpv_tdrXMZuTBWAA` — Jaime El Barco — Otto-Schütz-Weg 5, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZehDEfIpv_tdrXMZuTBWAA",
    "businessname": "Jaime El Barco",
    "address": "Otto-Schütz-Weg 5, 8050 Zürich"
  }
  JSON
  ```

- [ ] `SoUa0szgz3SZL7jigq8ZZg` — Restaurant Rosi — Sihlfeldstrasse 89, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "SoUa0szgz3SZL7jigq8ZZg",
    "businessname": "Restaurant Rosi",
    "address": "Sihlfeldstrasse 89, 8004 Zürich"
  }
  JSON
  ```

- [ ] `0PuaRwY2oBBqcf4C0lsIDw` — Bubbles — Werdstrasse 54, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0PuaRwY2oBBqcf4C0lsIDw",
    "businessname": "Bubbles",
    "address": "Werdstrasse 54, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Xrzcd_fzchn0y1nhORnXNQ` — Astra Kitchen & Bar — Löwenstrasse 25, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Xrzcd_fzchn0y1nhORnXNQ",
    "businessname": "Astra Kitchen & Bar",
    "address": "Löwenstrasse 25, 8001 Zürich"
  }
  JSON
  ```

- [ ] `cfuNusCpHwrDBjbw8Nmk6A` — Restaurant Tschingg Oerlikon — Schaffhauserstrasse 353, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cfuNusCpHwrDBjbw8Nmk6A",
    "businessname": "Restaurant Tschingg Oerlikon",
    "address": "Schaffhauserstrasse 353, 8050 Zürich"
  }
  JSON
  ```

- [ ] `HEQfKX7yuZGEUMQHfQaUcQ` — Confiserie Baumann AG — Balgriststrasse 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HEQfKX7yuZGEUMQHfQaUcQ",
    "businessname": "Confiserie Baumann AG",
    "address": "Balgriststrasse 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `F5hI5F2ncnuWlrOb7cUEvw` — Restaurant Lalina Ag — Thurgauerstrasse 23, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "F5hI5F2ncnuWlrOb7cUEvw",
    "businessname": "Restaurant Lalina Ag",
    "address": "Thurgauerstrasse 23, 8050 Zürich"
  }
  JSON
  ```

- [ ] `Oc7WK8XJQHBGsH4vq1JG1A` — Burgstein's Gasthaus Penalty — Hallwylstrasse 40, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Oc7WK8XJQHBGsH4vq1JG1A",
    "businessname": "Burgstein's Gasthaus Penalty",
    "address": "Hallwylstrasse 40, 8004 Zürich"
  }
  JSON
  ```

- [ ] `-ZSdi9Me9HG5w2Xe5FnA5g` — Bros Beans & Beats — Gartenhofstrasse 24, 8004 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-ZSdi9Me9HG5w2Xe5FnA5g",
    "businessname": "Bros Beans & Beats",
    "address": "Gartenhofstrasse 24, 8004 Zürich"
  }
  JSON
  ```

- [ ] `l1tWUuiVfxuTq0FmtASkdw` — Fu Lin Asia Restaurant — Hohlstrasse 189, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "l1tWUuiVfxuTq0FmtASkdw",
    "businessname": "Fu Lin Asia Restaurant",
    "address": "Hohlstrasse 189, 8004 Zürich"
  }
  JSON
  ```

- [ ] `UptxdqVG4rdLPNZAHhnY2w` — Fulin — Hohlstrasse 189, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "UptxdqVG4rdLPNZAHhnY2w",
    "businessname": "Fulin",
    "address": "Hohlstrasse 189, 8004 Zürich"
  }
  JSON
  ```

- [ ] `mTNO45RB1eoYO2woehsq1g` — Vongole’s Kitchen — Forchstrasse 225, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "mTNO45RB1eoYO2woehsq1g",
    "businessname": "Vongole’s Kitchen",
    "address": "Forchstrasse 225, 8032 Zürich"
  }
  JSON
  ```

- [ ] `TthHp0O8rk7huRWPqFdZ0w` — Huusbeiz — Badenerstrasse 310, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "TthHp0O8rk7huRWPqFdZ0w",
    "businessname": "Huusbeiz",
    "address": "Badenerstrasse 310, 8004 Zürich"
  }
  JSON
  ```

- [ ] `XljInGjeCkOaoKqh3LIKkw` — Popeyes Louisiana Kitchen — Baslerstrasse 50, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XljInGjeCkOaoKqh3LIKkw",
    "businessname": "Popeyes Louisiana Kitchen",
    "address": "Baslerstrasse 50, 8048 Zürich"
  }
  JSON
  ```

- [ ] `ra5VJyI3_VeREaqnSncz2w` — Kochstudio Mangostan L. Richter — Albisriederstrasse 182a, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ra5VJyI3_VeREaqnSncz2w",
    "businessname": "Kochstudio Mangostan L. Richter",
    "address": "Albisriederstrasse 182a, 8047 Zürich"
  }
  JSON
  ```

- [ ] `_f3C-Y0mtyT_W_JNibaayg` — Restaurant Gandria — Rudolfstrasse 6, 8008 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_f3C-Y0mtyT_W_JNibaayg",
    "businessname": "Restaurant Gandria",
    "address": "Rudolfstrasse 6, 8008 Zürich"
  }
  JSON
  ```

- [ ] `gBnbFY8jTgq9otHf6FJM-A` — Café Restaurant Mühlebach — Mühlebachstrasse 43, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gBnbFY8jTgq9otHf6FJM-A",
    "businessname": "Café Restaurant Mühlebach",
    "address": "Mühlebachstrasse 43, 8008 Zürich"
  }
  JSON
  ```

- [ ] `0HVEL1zybwBsZZ8VgcDyJg` — Test_Nast — H 120, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0HVEL1zybwBsZZ8VgcDyJg",
    "businessname": "Test_Nast",
    "address": "H 120, 8005 Zürich"
  }
  JSON
  ```

- [ ] `iswaq9ZflA7yIzwJl9nOyA` — Wirtschaft Ziegelhütte — Hüttenkopfstrasse 70, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "iswaq9ZflA7yIzwJl9nOyA",
    "businessname": "Wirtschaft Ziegelhütte",
    "address": "Hüttenkopfstrasse 70, 8051 Zürich"
  }
  JSON
  ```

- [ ] `qM5aUF84g4qduM6l4h5ZrQ` — Zum Roten Kamel — Niederdorfstrasse 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qM5aUF84g4qduM6l4h5ZrQ",
    "businessname": "Zum Roten Kamel",
    "address": "Niederdorfstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `yHze1dYraNOaiKNW0vL2hg` — Chickeria Langstrasse — Langstrasse 83, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yHze1dYraNOaiKNW0vL2hg",
    "businessname": "Chickeria Langstrasse",
    "address": "Langstrasse 83, 8004 Zürich"
  }
  JSON
  ```

- [ ] `KEH3iuvc3i4TdGGnbjEQSA` — Gasthof Hirschen — Winterthurerstrasse 519, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KEH3iuvc3i4TdGGnbjEQSA",
    "businessname": "Gasthof Hirschen",
    "address": "Winterthurerstrasse 519, 8051 Zürich"
  }
  JSON
  ```

- [ ] `ONFzzxtBCES3Gg-uNit5qQ` — McDonald's Restaurant — Kalanderplatz 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ONFzzxtBCES3Gg-uNit5qQ",
    "businessname": "McDonald's Restaurant",
    "address": "Kalanderplatz 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `hykxwoj8BRPfwtivczTxwA` — Bauschänzli — Stadthausquai 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "hykxwoj8BRPfwtivczTxwA",
    "businessname": "Bauschänzli",
    "address": "Stadthausquai 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `pAMZWEV56zOsxYF4mlYJjg` — Hong Kong Vertex AG — Thurgauerstrasse 32, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pAMZWEV56zOsxYF4mlYJjg",
    "businessname": "Hong Kong Vertex AG",
    "address": "Thurgauerstrasse 32, 8050 Zürich"
  }
  JSON
  ```

- [ ] `y5ABRQ6qwPJLZC_lnnhpHg` — Metzg — Seefeldstrasse 159, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "y5ABRQ6qwPJLZC_lnnhpHg",
    "businessname": "Metzg",
    "address": "Seefeldstrasse 159, 8008 Zürich"
  }
  JSON
  ```

- [ ] `weWnQ28e7x-Bp4cOl8cJyg` — barfussbar — Stadthausquai 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "weWnQ28e7x-Bp4cOl8cJyg",
    "businessname": "barfussbar",
    "address": "Stadthausquai 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `p2ivIzD5-VdBZUT6S-QHZw` — Yalla Habibi 2 Restaurant & Shisha Lounge — Birmensdorferstrasse 191, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "p2ivIzD5-VdBZUT6S-QHZw",
    "businessname": "Yalla Habibi 2 Restaurant & Shisha Lounge",
    "address": "Birmensdorferstrasse 191, 8003 Zürich"
  }
  JSON
  ```

- [ ] `BKdhExXVUTQokyu5XdDQsQ` — Restaurant Blume — Winterthurerstrasse 534, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "BKdhExXVUTQokyu5XdDQsQ",
    "businessname": "Restaurant Blume",
    "address": "Winterthurerstrasse 534, 8051 Zürich"
  }
  JSON
  ```

- [ ] `nMluoL5Z7jnTIq4Tjp_RgA` — Mère Catherine — Nägelihof 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nMluoL5Z7jnTIq4Tjp_RgA",
    "businessname": "Mère Catherine",
    "address": "Nägelihof 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `aR3Y2bYC5D5RVrLF-HhxlA` — Café Odno — Kreuzstrasse 26, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "aR3Y2bYC5D5RVrLF-HhxlA",
    "businessname": "Café Odno",
    "address": "Kreuzstrasse 26, 8008 Zürich"
  }
  JSON
  ```

- [ ] `VdhiHcfkVU2DzGZXbl_mKw` — Enzian Cafébar Main Tower — Thurgauerstrasse 36, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VdhiHcfkVU2DzGZXbl_mKw",
    "businessname": "Enzian Cafébar Main Tower",
    "address": "Thurgauerstrasse 36, 8050 Zürich"
  }
  JSON
  ```

- [ ] `jw62SZCUzDMUwuinnpY7hw` — Burger King — Niederdorfstrasse 30, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jw62SZCUzDMUwuinnpY7hw",
    "businessname": "Burger King",
    "address": "Niederdorfstrasse 30, 8001 Zürich"
  }
  JSON
  ```

- [ ] `ldZEiJRavmI_z3T1KNy80Q` — Shinwazen — Freischützgasse 10, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ldZEiJRavmI_z3T1KNy80Q",
    "businessname": "Shinwazen",
    "address": "Freischützgasse 10, 8004 Zürich"
  }
  JSON
  ```

- [ ] `adetcCrdgW5oB2OWoWOKrQ` — Don Quijote — Brauerstrasse 36, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "adetcCrdgW5oB2OWoWOKrQ",
    "businessname": "Don Quijote",
    "address": "Brauerstrasse 36, 8004 Zürich"
  }
  JSON
  ```

- [ ] `BN5dwXTZ8G1lOXilwHtApA` — EAT.ch GmbH — Manessestrasse 85, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "BN5dwXTZ8G1lOXilwHtApA",
    "businessname": "EAT.ch GmbH",
    "address": "Manessestrasse 85, 8045 Zürich"
  }
  JSON
  ```

- [ ] `ySUAP9_-A42vuQZSvDtR6w` — Cheti's Curry — Seefeldstrasse 7, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ySUAP9_-A42vuQZSvDtR6w",
    "businessname": "Cheti's Curry",
    "address": "Seefeldstrasse 7, 8008 Zürich"
  }
  JSON
  ```

- [ ] `xNnGmtfex_kqeo4TX4g31Q` — Ristorante Napoli — Sandstrasse 7, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xNnGmtfex_kqeo4TX4g31Q",
    "businessname": "Ristorante Napoli",
    "address": "Sandstrasse 7, 8003 Zürich"
  }
  JSON
  ```

- [ ] `6rU96lpXhSsGWfY8TTvNDQ` — Küchenwerkstatt — Oberdorfstrasse 22, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6rU96lpXhSsGWfY8TTvNDQ",
    "businessname": "Küchenwerkstatt",
    "address": "Oberdorfstrasse 22, 8001 Zürich"
  }
  JSON
  ```

- [ ] `8_bWr7 3tjEHrLq2WsIpWHw` — Ristorante Totò — Seefeldstrasse 124, 8008 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8_bWr7 3tjEHrLq2WsIpWHw",
    "businessname": "Ristorante Totò",
    "address": "Seefeldstrasse 124, 8008 Zürich"
  }
  JSON
  ```

- [ ] `5AcOgkWzPtMCZCA_nUfeOg` — Tokyo Tapas — Zwinglistrasse 3, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5AcOgkWzPtMCZCA_nUfeOg",
    "businessname": "Tokyo Tapas",
    "address": "Zwinglistrasse 3, 8004 Zürich"
  }
  JSON
  ```

- [ ] `gtGxEOa6b6yn2wtorMhlFg` — Ristorante Vallocaia — Niederdorfstrasse 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gtGxEOa6b6yn2wtorMhlFg",
    "businessname": "Ristorante Vallocaia",
    "address": "Niederdorfstrasse 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HTkrD9qpZrdZD12_9tssKg` — Canzoniere — Kanzleistrasse 84, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HTkrD9qpZrdZD12_9tssKg",
    "businessname": "Canzoniere",
    "address": "Kanzleistrasse 84, 8004 Zürich"
  }
  JSON
  ```

- [ ] `ovqHcxd1j1tAfpmJHRYOrg` — THE YARD Restaurant & Hotel — Bäckerstrasse 62, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ovqHcxd1j1tAfpmJHRYOrg",
    "businessname": "THE YARD Restaurant & Hotel",
    "address": "Bäckerstrasse 62, 8004 Zürich"
  }
  JSON
  ```

- [ ] `auVJlp4bhGSHrjf9IdjUoQ` — Bar 63 GmbH — Rolandstrasse 19, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "auVJlp4bhGSHrjf9IdjUoQ",
    "businessname": "Bar 63 GmbH",
    "address": "Rolandstrasse 19, 8004 Zürich"
  }
  JSON
  ```

- [ ] `qkDt0q6EcjjBl6izn9BUOA` — Restaurant Hirschen Serhan Safran — Waldstrasse 9, 8046 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qkDt0q6EcjjBl6izn9BUOA",
    "businessname": "Restaurant Hirschen Serhan Safran",
    "address": "Waldstrasse 9, 8046 Zürich"
  }
  JSON
  ```

- [ ] `V399T8wwL9xOub-_cUI1FQ` — YOYO Pizza — Friesenbergstrasse 12, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "V399T8wwL9xOub-_cUI1FQ",
    "businessname": "YOYO Pizza",
    "address": "Friesenbergstrasse 12, 8055 Zürich"
  }
  JSON
  ```

- [ ] `xfX9KLfqOwtc5qZr0mncBg` — Liquid-Bar — Zwinglistrasse 12, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xfX9KLfqOwtc5qZr0mncBg",
    "businessname": "Liquid-Bar",
    "address": "Zwinglistrasse 12, 8004 Zürich"
  }
  JSON
  ```

- [ ] `g02HKKVdWsmf_LVnIiMAfA` — Restaurant Jägerburg — Molkenstrasse 20, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "g02HKKVdWsmf_LVnIiMAfA",
    "businessname": "Restaurant Jägerburg",
    "address": "Molkenstrasse 20, 8004 Zürich"
  }
  JSON
  ```

- [ ] `9ihqYKLAXMg0KKj8b0WZwQ` — Gül — Tellstrasse 22, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "9ihqYKLAXMg0KKj8b0WZwQ",
    "businessname": "Gül",
    "address": "Tellstrasse 22, 8004 Zürich"
  }
  JSON
  ```

- [ ] `oVEjsPgiwXS-c2KqeO0FaA` — blindekuh — Mühlebachstrasse 148, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "oVEjsPgiwXS-c2KqeO0FaA",
    "businessname": "blindekuh",
    "address": "Mühlebachstrasse 148, 8008 Zürich"
  }
  JSON
  ```

- [ ] `rPs42JlyMK6zuDlCzLm1MA` — Restaurant Milano — Militärstrasse 109, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rPs42JlyMK6zuDlCzLm1MA",
    "businessname": "Restaurant Milano",
    "address": "Militärstrasse 109, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nK9tVWe6dw14uf6lALSxKg` — Casco Viejo — Rosengasse 7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nK9tVWe6dw14uf6lALSxKg",
    "businessname": "Casco Viejo",
    "address": "Rosengasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `KCE9CC9se8RCv9M3Izutyw` — Yalda Sihlcity — Kalanderplatz 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KCE9CC9se8RCv9M3Izutyw",
    "businessname": "Yalda Sihlcity",
    "address": "Kalanderplatz 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `_o5FfFWQvqTdXsbZGsCzmA` — Take Away-Pizza Sihlpassage — Passage Sihlquai, 8004 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_o5FfFWQvqTdXsbZGsCzmA",
    "businessname": "Take Away-Pizza Sihlpassage",
    "address": "Passage Sihlquai, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Pf7515oobiyFDV63ff_vgA` — Bistro Kafi — Stauffacherstrasse 141, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Pf7515oobiyFDV63ff_vgA",
    "businessname": "Bistro Kafi",
    "address": "Stauffacherstrasse 141, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nQAdxmbPfr4rzoFgWE15Eg` — Bistro Horizont — Mühlebachstrasse 112, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nQAdxmbPfr4rzoFgWE15Eg",
    "businessname": "Bistro Horizont",
    "address": "Mühlebachstrasse 112, 8008 Zürich"
  }
  JSON
  ```

- [ ] `usbo-rCtqgCqg7orAwFBHg` — dieci Gelateria & Take Away — Niederdorfstrasse 40, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "usbo-rCtqgCqg7orAwFBHg",
    "businessname": "dieci Gelateria & Take Away",
    "address": "Niederdorfstrasse 40, 8001 Zürich"
  }
  JSON
  ```

- [ ] `4qaTdBE46YdFOtjPr2_DEQ` — Veganitas Restaurant — Brauerstrasse 30, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4qaTdBE46YdFOtjPr2_DEQ",
    "businessname": "Veganitas Restaurant",
    "address": "Brauerstrasse 30, 8004 Zürich"
  }
  JSON
  ```

- [ ] `-908eq4-ve5VXghCFHXxOg` — WonderWaffel & Coffee Zürich — Seefeldstrasse 40, 8008 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-908eq4-ve5VXghCFHXxOg",
    "businessname": "WonderWaffel & Coffee Zürich",
    "address": "Seefeldstrasse 40, 8008 Zürich"
  }
  JSON
  ```

- [ ] `Ljf4h79bF0w712-1K1eOPQ` — Toro Bar — Schöneggstrasse 25, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Ljf4h79bF0w712-1K1eOPQ",
    "businessname": "Toro Bar",
    "address": "Schöneggstrasse 25, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Ky5_rAIEEqxV_-oi-galGg` — Art 4 Bar - Music & Lounge — Kanonengasse 15, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Ky5_rAIEEqxV_-oi-galGg",
    "businessname": "Art 4 Bar - Music & Lounge",
    "address": "Kanonengasse 15, 8004 Zürich"
  }
  JSON
  ```

- [ ] `uHLb0JLUfhYgM8JWVlgcVw` — Cafeteria Bar-A-Graph — Badenerstrasse 90, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "uHLb0JLUfhYgM8JWVlgcVw",
    "businessname": "Cafeteria Bar-A-Graph",
    "address": "Badenerstrasse 90, 8004 Zürich"
  }
  JSON
  ```

- [ ] `M47T9QxIgcsw0KgnZR6ZpQ` — YALDA Europaallee — Gustav-Gull-Platz 2, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "M47T9QxIgcsw0KgnZR6ZpQ",
    "businessname": "YALDA Europaallee",
    "address": "Gustav-Gull-Platz 2, 8004 Zürich"
  }
  JSON
  ```

- [ ] `_kHybsmrFbi5Aub_2v5m3Q` — Bäckerei Urs Vohdin — Oberdorfstrasse 12, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_kHybsmrFbi5Aub_2v5m3Q",
    "businessname": "Bäckerei Urs Vohdin",
    "address": "Oberdorfstrasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `X6-6GqDtUkshhqetEE8_kQ` — Igniv Zurich by Andreas Caminada — Marktgasse 17, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "X6-6GqDtUkshhqetEE8_kQ",
    "businessname": "Igniv Zurich by Andreas Caminada",
    "address": "Marktgasse 17, 8001 Zürich"
  }
  JSON
  ```

- [ ] `g0CGeMCH3xlhIB_3RQ0U8g` — Shinwazen — Freischützgasse 10, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "g0CGeMCH3xlhIB_3RQ0U8g",
    "businessname": "Shinwazen",
    "address": "Freischützgasse 10, 8004 Zürich"
  }
  JSON
  ```

- [ ] `ptk6N1ex9Iyr_7tZI_2h3w` — EGE Import & Export GmbH — Feldstrasse 133, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ptk6N1ex9Iyr_7tZI_2h3w",
    "businessname": "EGE Import & Export GmbH",
    "address": "Feldstrasse 133, 8004 Zürich"
  }
  JSON
  ```

- [ ] `fjCnReANp7u9XOqq7Kpw1g` — Sultan Sofrasi — Wehntalerstrasse 280, 8046 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fjCnReANp7u9XOqq7Kpw1g",
    "businessname": "Sultan Sofrasi",
    "address": "Wehntalerstrasse 280, 8046 Zürich"
  }
  JSON
  ```

- [ ] `HCXHXqM7erqTa8QXksfiPQ` — Tiffins — Seefeldstrasse 61, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HCXHXqM7erqTa8QXksfiPQ",
    "businessname": "Tiffins",
    "address": "Seefeldstrasse 61, 8008 Zürich"
  }
  JSON
  ```

- [ ] `3xfEXKuxGS8FAvwrTxzgiw` — Thai Heaven — Stüssihofstatt 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3xfEXKuxGS8FAvwrTxzgiw",
    "businessname": "Thai Heaven",
    "address": "Stüssihofstatt 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `JMVQHZUDsbH_Y5WcNQ1FYQ` — Restaurant Rechberg 1837 — Chorgasse 20, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JMVQHZUDsbH_Y5WcNQ1FYQ",
    "businessname": "Restaurant Rechberg 1837",
    "address": "Chorgasse 20, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HWfhJncADRkaVrGNgzYvfQ` — Restaurant Chez Dannys — Anemonenstrasse, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HWfhJncADRkaVrGNgzYvfQ",
    "businessname": "Restaurant Chez Dannys",
    "address": "Anemonenstrasse, 8047 Zürich"
  }
  JSON
  ```

- [ ] `PxwPSUGWSjsCHEdlvVuhCA` — yume-ramen gmbh — Reitergasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "PxwPSUGWSjsCHEdlvVuhCA",
    "businessname": "yume-ramen gmbh",
    "address": "Reitergasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `UKwPcbc3XUJdzGNCiLANmg` — NZZ Café — Dock A 2472, 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "UKwPcbc3XUJdzGNCiLANmg",
    "businessname": "NZZ Café",
    "address": "Dock A 2472, 8060 Zürich"
  }
  JSON
  ```

- [ ] `8cYIDy3G2YdO0CptIloEkQ` — Pizza Restaurant Rosa — Birmensdorferstrasse 249, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8cYIDy3G2YdO0CptIloEkQ",
    "businessname": "Pizza Restaurant Rosa",
    "address": "Birmensdorferstrasse 249, 8055 Zürich"
  }
  JSON
  ```

- [ ] `jmHXZNXCHm0Y0twX2v8Udw` — Family Grill GmbH — Bahnhaldenstrasse 2a, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jmHXZNXCHm0Y0twX2v8Udw",
    "businessname": "Family Grill GmbH",
    "address": "Bahnhaldenstrasse 2a, 8052 Zürich"
  }
  JSON
  ```

- [ ] `2l2sfrjRGrwkTAsaF_dHHA` — Limmathof — Limmatstrasse 217, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2l2sfrjRGrwkTAsaF_dHHA",
    "businessname": "Limmathof",
    "address": "Limmatstrasse 217, 8005 Zürich"
  }
  JSON
  ```

- [ ] `7GnxlaYYCJQbyZYuEPlUZQ` — Ona Poké — Bleicherweg 19, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7GnxlaYYCJQbyZYuEPlUZQ",
    "businessname": "Ona Poké",
    "address": "Bleicherweg 19, 8002 Zürich"
  }
  JSON
  ```

- [ ] `0mY2oqm3pSf6gXctSk10Hg` — Ristorante Pizzeria Tramblu — Bucheggstrasse 103, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0mY2oqm3pSf6gXctSk10Hg",
    "businessname": "Ristorante Pizzeria Tramblu",
    "address": "Bucheggstrasse 103, 8057 Zürich"
  }
  JSON
  ```

- [ ] `Qh87cFuRbqgG70GApIGgEA` — Restaurant Emilio Weinhandlung AG — Zweierstrasse 9, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Qh87cFuRbqgG70GApIGgEA",
    "businessname": "Restaurant Emilio Weinhandlung AG",
    "address": "Zweierstrasse 9, 8004 Zürich"
  }
  JSON
  ```

- [ ] `C0BRR7JRc6hICrjhDykWxw` — Café Z am Park — Zurlindenstrasse 275, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "C0BRR7JRc6hICrjhDykWxw",
    "businessname": "Café Z am Park",
    "address": "Zurlindenstrasse 275, 8003 Zürich"
  }
  JSON
  ```

- [ ] `9ioi08AZWL9wC-dqoocM2Q` — Restaurant Römerblick — Asylstrasse 58, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "9ioi08AZWL9wC-dqoocM2Q",
    "businessname": "Restaurant Römerblick",
    "address": "Asylstrasse 58, 8032 Zürich"
  }
  JSON
  ```

- [ ] `SCabBm-sowavrRGV6lALhQ` — Salir — Hottingerstrasse 27, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "SCabBm-sowavrRGV6lALhQ",
    "businessname": "Salir",
    "address": "Hottingerstrasse 27, 8032 Zürich"
  }
  JSON
  ```

- [ ] `iNNcM1MgpXZG7WLY8bMHeQ` — Delhihouse Of Be stcurry Restaurant — Zypressenstrasse 52, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "iNNcM1MgpXZG7WLY8bMHeQ",
    "businessname": "Delhihouse Of Be stcurry Restaurant",
    "address": "Zypressenstrasse 52, 8004 Zürich"
  }
  JSON
  ```

- [ ] `EOtLvWO5D-7yMI4za4ozDg` — Il Grappolo — Widmerstrasse 64, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EOtLvWO5D-7yMI4za4ozDg",
    "businessname": "Il Grappolo",
    "address": "Widmerstrasse 64, 8038 Zürich"
  }
  JSON
  ```

- [ ] `Sl4SXhwDmePPNBlY6eBaPw` — Maiden Shanghai Zurich — Döltschiweg 234, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Sl4SXhwDmePPNBlY6eBaPw",
    "businessname": "Maiden Shanghai Zurich",
    "address": "Döltschiweg 234, 8055 Zürich"
  }
  JSON
  ```

- [ ] `0bW684mEAoK3oYlI2ctNsw` — Kafi Linde — Bachstrasse 10, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0bW684mEAoK3oYlI2ctNsw",
    "businessname": "Kafi Linde",
    "address": "Bachstrasse 10, 8038 Zürich"
  }
  JSON
  ```

- [ ] `15xDm2BA-0qaCB3QH7_gBA` — Restaurant Grünwald — Regensdorferstrasse 237, 8049 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "15xDm2BA-0qaCB3QH7_gBA",
    "businessname": "Restaurant Grünwald",
    "address": "Regensdorferstrasse 237, 8049 Zürich"
  }
  JSON
  ```

- [ ] `62gbz57eXz5y8rb3RkR69A` — Cafeteria UZH Tierspital — Winterthurerstrasse 260, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "62gbz57eXz5y8rb3RkR69A",
    "businessname": "Cafeteria UZH Tierspital",
    "address": "Winterthurerstrasse 260, 8057 Zürich"
  }
  JSON
  ```

- [ ] `HlgVa7CYjnwAh8Xj9ShJ0w` — Si o No — Ankerstrasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HlgVa7CYjnwAh8Xj9ShJ0w",
    "businessname": "Si o No",
    "address": "Ankerstrasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `lSZqJGOSyZRAYPzkuq53CQ` — GRAND CAFÉ LOCHERGUT — Badenerstrasse 230, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lSZqJGOSyZRAYPzkuq53CQ",
    "businessname": "GRAND CAFÉ LOCHERGUT",
    "address": "Badenerstrasse 230, 8004 Zürich"
  }
  JSON
  ```

- [ ] `6qQzgrx_ewihPHrGhuuKcA` — Silberkugel: — Franklinstrasse 11, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6qQzgrx_ewihPHrGhuuKcA",
    "businessname": "Silberkugel:",
    "address": "Franklinstrasse 11, 8050 Zürich"
  }
  JSON
  ```

- [ ] `s3A2S7NmncexNOdCM1gdqg` — ApéRoyal GmbH — Tödistrasse 44, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "s3A2S7NmncexNOdCM1gdqg",
    "businessname": "ApéRoyal GmbH",
    "address": "Tödistrasse 44, 8002 Zürich"
  }
  JSON
  ```

- [ ] `XGoiUSdoNXaHG7en2z5IIg` — Degenried Restaurant Wirtschaft — Degenriedstrasse 135, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XGoiUSdoNXaHG7en2z5IIg",
    "businessname": "Degenried Restaurant Wirtschaft",
    "address": "Degenriedstrasse 135, 8032 Zürich"
  }
  JSON
  ```

- [ ] `jXCMlWFMuOgsMA8sNDqE3A` — Monti's Bistro — Birmensdorferstrasse 486/488, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jXCMlWFMuOgsMA8sNDqE3A",
    "businessname": "Monti's Bistro",
    "address": "Birmensdorferstrasse 486/488, 8055 Zürich"
  }
  JSON
  ```

- [ ] `R1gtxd2fzcsnKaj3SEOvdg` — Le Raymond Bar — Bleicherweg 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "R1gtxd2fzcsnKaj3SEOvdg",
    "businessname": "Le Raymond Bar",
    "address": "Bleicherweg 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `aFbc4kma5oZp0eyxbOSAGQ` — Belcafé Pizza und Bar — Bellevueplatz 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "aFbc4kma5oZp0eyxbOSAGQ",
    "businessname": "Belcafé Pizza und Bar",
    "address": "Bellevueplatz 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `GAKVBYPkbPFY-z0Hxws3uw` — Restaurant Seerose — Seestrasse 493, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GAKVBYPkbPFY-z0Hxws3uw",
    "businessname": "Restaurant Seerose",
    "address": "Seestrasse 493, 8038 Zürich"
  }
  JSON
  ```

- [ ] `TkeCyV7tFHc_wafObM6Ebg` — OYU Restaurant — Sihlstrasse 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "TkeCyV7tFHc_wafObM6Ebg",
    "businessname": "OYU Restaurant",
    "address": "Sihlstrasse 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `rVcbO7l9-Qk24OiEzTjxog` — Wühre Restaurant — Wühre 11, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rVcbO7l9-Qk24OiEzTjxog",
    "businessname": "Wühre Restaurant",
    "address": "Wühre 11, 8001 Zürich"
  }
  JSON
  ```

- [ ] `J6RFpyVvZPj8mm02cWKdPQ` — Hiltl Pflanzbar — Talstrasse 62, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "J6RFpyVvZPj8mm02cWKdPQ",
    "businessname": "Hiltl Pflanzbar",
    "address": "Talstrasse 62, 8001 Zürich"
  }
  JSON
  ```

- [ ] `yZ2tDMSfJ43eTmBGxhv7dA` — Sala of Tokyo — Schützengasse 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yZ2tDMSfJ43eTmBGxhv7dA",
    "businessname": "Sala of Tokyo",
    "address": "Schützengasse 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `vfd5yOh5xNcOvTGbUvGPtg` — Napi‘s — Flurstrasse 4, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vfd5yOh5xNcOvTGbUvGPtg",
    "businessname": "Napi‘s",
    "address": "Flurstrasse 4, 8048 Zürich"
  }
  JSON
  ```

- [ ] `E3H1PB6YbgaqGFezZh1QgQ` — GIESSEREI OERLIKON — Birchstrasse 108, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "E3H1PB6YbgaqGFezZh1QgQ",
    "businessname": "GIESSEREI OERLIKON",
    "address": "Birchstrasse 108, 8050 Zürich"
  }
  JSON
  ```

- [ ] `36diWUfVGP9cnv6_WARLKg` — Kraftwerk — Selnaustrasse 25, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "36diWUfVGP9cnv6_WARLKg",
    "businessname": "Kraftwerk",
    "address": "Selnaustrasse 25, 8001 Zürich"
  }
  JSON
  ```

- [ ] `pzZSuui-6iK0T5lCFdTcMQ` — Restaurant Sonne Libanon — Altstetterstrasse 223, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pzZSuui-6iK0T5lCFdTcMQ",
    "businessname": "Restaurant Sonne Libanon",
    "address": "Altstetterstrasse 223, 8048 Zürich"
  }
  JSON
  ```

- [ ] `lvJxzKgsRKg06T1uLkSolQ` — VIOR Zürich — Löwenstrasse 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lvJxzKgsRKg06T1uLkSolQ",
    "businessname": "VIOR Zürich",
    "address": "Löwenstrasse 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CiUwUquR8ipFGZLzsihjjg` — Globus Bellevue — Theaterstrasse 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CiUwUquR8ipFGZLzsihjjg",
    "businessname": "Globus Bellevue",
    "address": "Theaterstrasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `XjuGFvMaRhDiLcBF_p9Mlg` — Shilla — Badenerstrasse 505, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XjuGFvMaRhDiLcBF_p9Mlg",
    "businessname": "Shilla",
    "address": "Badenerstrasse 505, 8048 Zürich"
  }
  JSON
  ```

- [ ] `RJhTOnZ75lFFl0lMZTNlaw` — Paninoteca La Penisola — Giessereistrasse 18, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RJhTOnZ75lFFl0lMZTNlaw",
    "businessname": "Paninoteca La Penisola",
    "address": "Giessereistrasse 18, 8005 Zürich"
  }
  JSON
  ```

- [ ] `97YU_Ll24wbtYgJyoSKs_w` — Confiserie Cafe Bauer — Badenerstrasse 355, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "97YU_Ll24wbtYgJyoSKs_w",
    "businessname": "Confiserie Cafe Bauer",
    "address": "Badenerstrasse 355, 8003 Zürich"
  }
  JSON
  ```

- [ ] `41hM3ZuJHIevoqEbEGSZCw` — Ristorante Klingler's — Münzplatz 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "41hM3ZuJHIevoqEbEGSZCw",
    "businessname": "Ristorante Klingler's",
    "address": "Münzplatz 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `zOVQdAlNAed86Yheh6wIAw` — Storchen Zürich — Weinplatz 2, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zOVQdAlNAed86Yheh6wIAw",
    "businessname": "Storchen Zürich",
    "address": "Weinplatz 2, 8001 Zürich"
  }
  JSON
  ```

- [ ] `OjL-lmig51PmGHhL8xEdXQ` — Restaurant Lunch 5 GmbH — Förrlibuckstrasse 62, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OjL-lmig51PmGHhL8xEdXQ",
    "businessname": "Restaurant Lunch 5 GmbH",
    "address": "Förrlibuckstrasse 62, 8005 Zürich"
  }
  JSON
  ```

- [ ] `R2WIIn_pm5F9d6RFIu_EsA` — Gerold Chuchi — Geroldstrasse 5, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "R2WIIn_pm5F9d6RFIu_EsA",
    "businessname": "Gerold Chuchi",
    "address": "Geroldstrasse 5, 8005 Zürich"
  }
  JSON
  ```

- [ ] `45Nzv0t5R8y0k26QticFpw` — Tibetasia — Quellenstrasse 6, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "45Nzv0t5R8y0k26QticFpw",
    "businessname": "Tibetasia",
    "address": "Quellenstrasse 6, 8005 Zürich"
  }
  JSON
  ```

- [ ] `JCbPG1BpxPmJDumdI6o9kA` — Bar Mau — Zypressenstrasse 36, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JCbPG1BpxPmJDumdI6o9kA",
    "businessname": "Bar Mau",
    "address": "Zypressenstrasse 36, 8003 Zürich"
  }
  JSON
  ```

- [ ] `5K8ymGWuJ6dVjDxSpHlNIA` — Pascals Diner — Bahnhofstrasse 1, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5K8ymGWuJ6dVjDxSpHlNIA",
    "businessname": "Pascals Diner",
    "address": "Bahnhofstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gca2BLQSsoUJSw6tO5f7Jw` — Long Huang — Talstrasse 83, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gca2BLQSsoUJSw6tO5f7Jw",
    "businessname": "Long Huang",
    "address": "Talstrasse 83, 8001 Zürich"
  }
  JSON
  ```

- [ ] `80t2V0TEVXGmgPadwYKglg` — Ali Baba — Josefstrasse 91, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "80t2V0TEVXGmgPadwYKglg",
    "businessname": "Ali Baba",
    "address": "Josefstrasse 91, 8005 Zürich"
  }
  JSON
  ```

- [ ] `ri9WOIWVPYmxa3Xn1eb5vw` — Snack New Point — Langstrasse 206, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ri9WOIWVPYmxa3Xn1eb5vw",
    "businessname": "Snack New Point",
    "address": "Langstrasse 206, 8005 Zürich"
  }
  JSON
  ```

- [ ] `KvZ085B0lyCuyKHFk6TI2Q` — Restaurant Lotus Garden — Waffenplatzstrasse 1, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KvZ085B0lyCuyKHFk6TI2Q",
    "businessname": "Restaurant Lotus Garden",
    "address": "Waffenplatzstrasse 1, 8002 Zürich"
  }
  JSON
  ```

- [ ] `ue0McHK6_Azww1e0XCvGpw` — PURO - The Social Club — Fraumünsterstrasse 25, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ue0McHK6_Azww1e0XCvGpw",
    "businessname": "PURO - The Social Club",
    "address": "Fraumünsterstrasse 25, 8001 Zürich"
  }
  JSON
  ```

- [ ] `lcQRtfxfWcr6uUEdHZglGw` — Fleming's Club — Brandschenkestrasse 10, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lcQRtfxfWcr6uUEdHZglGw",
    "businessname": "Fleming's Club",
    "address": "Brandschenkestrasse 10, 8001 Zürich"
  }
  JSON
  ```

- [ ] `QDeZvsAw-ZGNEMw_6PADbw` — Ristorante Bindella — In Gassen 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "QDeZvsAw-ZGNEMw_6PADbw",
    "businessname": "Ristorante Bindella",
    "address": "In Gassen 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `O2y_gajTMINoI6R1WpWrgQ` — Widder Restaurant — Widdergasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "O2y_gajTMINoI6R1WpWrgQ",
    "businessname": "Widder Restaurant",
    "address": "Widdergasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `KBioOo0mUQ6Rabjr9Ib0jw` — Starbucks Coffee — Rennweg 48, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KBioOo0mUQ6Rabjr9Ib0jw",
    "businessname": "Starbucks Coffee",
    "address": "Rennweg 48, 8001 Zürich"
  }
  JSON
  ```

- [ ] `swz8pt6-7g8It4bn9EIx-g` — Churrasco — Glockengasse 9, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "swz8pt6-7g8It4bn9EIx-g",
    "businessname": "Churrasco",
    "address": "Glockengasse 9, 8001 Zürich"
  }
  JSON
  ```

- [ ] `K8z4Qzng40UH9HhM6jVDeg` — Lady Hamilton's Pub — Beatengasse 11, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "K8z4Qzng40UH9HhM6jVDeg",
    "businessname": "Lady Hamilton's Pub",
    "address": "Beatengasse 11, 8001 Zürich"
  }
  JSON
  ```

- [ ] `rto1WU-zHv1TtgO4nfDg5g` — Allegrotto — Bederstrasse 102, 8002  Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rto1WU-zHv1TtgO4nfDg5g",
    "businessname": "Allegrotto",
    "address": "Bederstrasse 102, 8002  Zürich"
  }
  JSON
  ```

- [ ] `KYyD1NaNA9Dk6P7d06lvyg` — Indian BBQ Restaurant & Bar — Breitensteinstrasse 21, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KYyD1NaNA9Dk6P7d06lvyg",
    "businessname": "Indian BBQ Restaurant & Bar",
    "address": "Breitensteinstrasse 21, 8037 Zürich"
  }
  JSON
  ```

- [ ] `juzho95er8Idnep0oU_OwQ` — Wüscht Beckerei-Konditorei-Confiseri 8041 Leimbach — Maneggstrasse 73, 8041 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "juzho95er8Idnep0oU_OwQ",
    "businessname": "Wüscht Beckerei-Konditorei-Confiseri 8041 Leimbach",
    "address": "Maneggstrasse 73, 8041 Zürich"
  }
  JSON
  ```

- [ ] `r5L4QXjM13efMiQp-hZYPQ` — Michel Frey Landschaftsarchitekten GmbH — Allmendstrasse 100, 8041 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "r5L4QXjM13efMiQp-hZYPQ",
    "businessname": "Michel Frey Landschaftsarchitekten GmbH",
    "address": "Allmendstrasse 100, 8041 Zürich"
  }
  JSON
  ```

- [ ] `iB5WsHKkug1reDzwomWIDw` — Sultanhan — Döltschihalde 31, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "iB5WsHKkug1reDzwomWIDw",
    "businessname": "Sultanhan",
    "address": "Döltschihalde 31, 8055 Zürich"
  }
  JSON
  ```

- [ ] `cf_0UnewV4IrxMmfrxnarA` — Fries Brothers — Langstrasse 238, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cf_0UnewV4IrxMmfrxnarA",
    "businessname": "Fries Brothers",
    "address": "Langstrasse 238, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Qc8aLFk26P-t1nDCmOeGoQ` — Dunkin' Donuts — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Qc8aLFk26P-t1nDCmOeGoQ",
    "businessname": "Dunkin' Donuts",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `39-FuyYTI-DrK4_6AZrx_Q` — Lima bar Zurich — Talacker 34, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "39-FuyYTI-DrK4_6AZrx_Q",
    "businessname": "Lima bar Zurich",
    "address": "Talacker 34, 8001 Zürich"
  }
  JSON
  ```

- [ ] `EwcLUydWMWS9W0CYdOtifw` — Restaurant Konshi — Uraniastrasse 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EwcLUydWMWS9W0CYdOtifw",
    "businessname": "Restaurant Konshi",
    "address": "Uraniastrasse 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `ed3ZrBUUtRoMrynjoyfxGQ` — Chiantiquelle — Stampfenbachstrasse 38, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ed3ZrBUUtRoMrynjoyfxGQ",
    "businessname": "Chiantiquelle",
    "address": "Stampfenbachstrasse 38, 8006 Zürich"
  }
  JSON
  ```

- [ ] `qybKuTS8vV4fhp4UZteAag` — Thali Indian Restaurant — Schaffhauserstrasse 32, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qybKuTS8vV4fhp4UZteAag",
    "businessname": "Thali Indian Restaurant",
    "address": "Schaffhauserstrasse 32, 8006 Zürich"
  }
  JSON
  ```

- [ ] `uWgSDTmFN5Zqp9qgV9b3QQ` — Dont Worry Eat Curry GmbH — Mattengasse 29, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "uWgSDTmFN5Zqp9qgV9b3QQ",
    "businessname": "Dont Worry Eat Curry GmbH",
    "address": "Mattengasse 29, 8005 Zürich"
  }
  JSON
  ```

- [ ] `_ENt6NS4KxaoHC3b_LuyTw` — Aperobar Freude — Limmatstrasse 254, 8005 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_ENt6NS4KxaoHC3b_LuyTw",
    "businessname": "Aperobar Freude",
    "address": "Limmatstrasse 254, 8005 Zürich"
  }
  JSON
  ```

- [ ] `eyr1oDANRUZclZILVnNtcw` — D-Vino Weinbars AG — Schützengasse 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "eyr1oDANRUZclZILVnNtcw",
    "businessname": "D-Vino Weinbars AG",
    "address": "Schützengasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Rg3Hqs_zciXmjJF0V3Wx6g` — Linde Oberstrass — Universitätstrasse 91, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Rg3Hqs_zciXmjJF0V3Wx6g",
    "businessname": "Linde Oberstrass",
    "address": "Universitätstrasse 91, 8006 Zürich"
  }
  JSON
  ```

- [ ] `Dm2QRk6Vsd3G-DjO-yLEWg` — Skebe — St. Urbangasse 4, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Dm2QRk6Vsd3G-DjO-yLEWg",
    "businessname": "Skebe",
    "address": "St. Urbangasse 4, 8001 Zürich"
  }
  JSON
  ```

- [ ] `2nSn6EaRx1g-s3Dta639GA` — Saltinbocca — Viaduktstrasse 52, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2nSn6EaRx1g-s3Dta639GA",
    "businessname": "Saltinbocca",
    "address": "Viaduktstrasse 52, 8005 Zürich"
  }
  JSON
  ```

- [ ] `DCR9CqIIFZJ6-gmyq3mcMw` — Hausammann — Universitätstrasse 88, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DCR9CqIIFZJ6-gmyq3mcMw",
    "businessname": "Hausammann",
    "address": "Universitätstrasse 88, 8006 Zürich"
  }
  JSON
  ```

- [ ] `BOHriit73-iLj5T6uAKEiA` — Scent of Bamboo — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "BOHriit73-iLj5T6uAKEiA",
    "businessname": "Scent of Bamboo",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `G26xaGZkLHDaWNecqfbX_Q` — Orsini — Waaggasse 7, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "G26xaGZkLHDaWNecqfbX_Q",
    "businessname": "Orsini",
    "address": "Waaggasse 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `i7_QjUHgvieUec4aC9a47Q` — Millennium — Limmatplatz 1, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "i7_QjUHgvieUec4aC9a47Q",
    "businessname": "Millennium",
    "address": "Limmatplatz 1, 8005 Zürich"
  }
  JSON
  ```

- [ ] `K-7GD-Yf_SOtxzcEiD3UCQ` — MIKI Ramen — Sihlfeldstrasse 63, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "K-7GD-Yf_SOtxzcEiD3UCQ",
    "businessname": "MIKI Ramen",
    "address": "Sihlfeldstrasse 63, 8003 Zürich"
  }
  JSON
  ```

- [ ] `rt8K0_GbXeR4Pccci1F3QQ` — Pery — Zentralstrasse 36, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rt8K0_GbXeR4Pccci1F3QQ",
    "businessname": "Pery",
    "address": "Zentralstrasse 36, 8003 Zürich"
  }
  JSON
  ```

- [ ] `ULXzywmZFPnbszfCJAdFtg` — Dalou — Viaduktstrasse 93, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ULXzywmZFPnbszfCJAdFtg",
    "businessname": "Dalou",
    "address": "Viaduktstrasse 93, 8005 Zürich"
  }
  JSON
  ```

- [ ] `HHgZIuD8MxwZJCRBYVKkHw` — Aroy Food GmbH — Hohlstrasse 556, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HHgZIuD8MxwZJCRBYVKkHw",
    "businessname": "Aroy Food GmbH",
    "address": "Hohlstrasse 556, 8048 Zürich"
  }
  JSON
  ```

- [ ] `2kMCNz8GsMguPP70chIo9w` — Willy's Fried Chicken — Badenerstrasse 540, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2kMCNz8GsMguPP70chIo9w",
    "businessname": "Willy's Fried Chicken",
    "address": "Badenerstrasse 540, 8048 Zürich"
  }
  JSON
  ```

- [ ] `Dxq3wjp8oUNzuaRORQVqOA` — Sterne Foifi — Theaterstrasse 22, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Dxq3wjp8oUNzuaRORQVqOA",
    "businessname": "Sterne Foifi",
    "address": "Theaterstrasse 22, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HQLyDwPlS64e6rYh8xrN6A` — Bamboo Inn — Culmannstrasse 19, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HQLyDwPlS64e6rYh8xrN6A",
    "businessname": "Bamboo Inn",
    "address": "Culmannstrasse 19, 8006 Zürich"
  }
  JSON
  ```

- [ ] `57XPzv-WhB_VNXUHYpZzlA` — Central Shisha Lounge — Stampfenbachstrasse 24, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "57XPzv-WhB_VNXUHYpZzlA",
    "businessname": "Central Shisha Lounge",
    "address": "Stampfenbachstrasse 24, 8001 Zürich"
  }
  JSON
  ```

- [ ] `i6OdEQxw4n3u2Cd9WKJZoQ` — Bar Basso — Sihlstrasse 59, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "i6OdEQxw4n3u2Cd9WKJZoQ",
    "businessname": "Bar Basso",
    "address": "Sihlstrasse 59, 8001 Zürich"
  }
  JSON
  ```

- [ ] `s0he8ZshCEcp70E3GrP_dg` — CLOUDS — Maagplatz 5, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "s0he8ZshCEcp70E3GrP_dg",
    "businessname": "CLOUDS",
    "address": "Maagplatz 5, 8005 Zürich"
  }
  JSON
  ```

- [ ] `DkvvZjobwMsSG5kPES6EnQ` — Restaurant Co Chin Chin — Gasometerstrasse 7, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DkvvZjobwMsSG5kPES6EnQ",
    "businessname": "Restaurant Co Chin Chin",
    "address": "Gasometerstrasse 7, 8005 Zürich"
  }
  JSON
  ```

- [ ] `IBb7mpHGnJDu2qCw7kk5GA` — Santa Lucia Limmatplatz — Luisenstrasse 31, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IBb7mpHGnJDu2qCw7kk5GA",
    "businessname": "Santa Lucia Limmatplatz",
    "address": "Luisenstrasse 31, 8005 Zürich"
  }
  JSON
  ```

- [ ] `BsdnLjzF3ZvAEoR9gcZl2g` — Restaurant Stapferstube Da Rizzo — Culmannstrasse 45, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "BsdnLjzF3ZvAEoR9gcZl2g",
    "businessname": "Restaurant Stapferstube Da Rizzo",
    "address": "Culmannstrasse 45, 8006 Zürich"
  }
  JSON
  ```

- [ ] `_O0MTaYK-C4paHqtEIrVlg` — Restaurant La Soupière — Bahnhofplatz 7, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_O0MTaYK-C4paHqtEIrVlg",
    "businessname": "Restaurant La Soupière",
    "address": "Bahnhofplatz 7, 8001 Zürich"
  }
  JSON
  ```

- [ ] `KsCc4QRzmXBlmXw_jq-ljg` — Yooji's Bellevue — St. Urbangasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KsCc4QRzmXBlmXw_jq-ljg",
    "businessname": "Yooji's Bellevue",
    "address": "St. Urbangasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `6eCt9rt1_BPVv1yzmWcnFw` — MyLocalina Showcase — Förrlibuckstrasse 62, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6eCt9rt1_BPVv1yzmWcnFw",
    "businessname": "MyLocalina Showcase",
    "address": "Förrlibuckstrasse 62, 8005 Zürich"
  }
  JSON
  ```

- [ ] `OBLZd1vAuWnCrte92zCsUg` — Theater 11 — Thurgauerstrasse 7, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OBLZd1vAuWnCrte92zCsUg",
    "businessname": "Theater 11",
    "address": "Thurgauerstrasse 7, 8050 Zürich"
  }
  JSON
  ```

- [ ] `fAYtAPHyMjByfRlrVRe2eg` — Negishi Sushi x Bento, Zürich Oerlikon — Hofwiesenstrasse 363, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fAYtAPHyMjByfRlrVRe2eg",
    "businessname": "Negishi Sushi x Bento, Zürich Oerlikon",
    "address": "Hofwiesenstrasse 363, 8050 Zürich"
  }
  JSON
  ```

- [ ] `aianc5HIA-lbqQE_wAoWZg` — Café Glättli — Glättlistrasse 40, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "aianc5HIA-lbqQE_wAoWZg",
    "businessname": "Café Glättli",
    "address": "Glättlistrasse 40, 8048 Zürich"
  }
  JSON
  ```

- [ ] `QDVJcbD3oq3-ua_ue0e1tA` — Franco Pizza Kurier Zürich — Wattstrasse 7, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "QDVJcbD3oq3-ua_ue0e1tA",
    "businessname": "Franco Pizza Kurier Zürich",
    "address": "Wattstrasse 7, 8050 Zürich"
  }
  JSON
  ```

- [ ] `JqQmjYR50DOBzaJ3BMiVlg` — Bagelboys Restaurant & Bakery — Dialogweg 11, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JqQmjYR50DOBzaJ3BMiVlg",
    "businessname": "Bagelboys Restaurant & Bakery",
    "address": "Dialogweg 11, 8050 Zürich"
  }
  JSON
  ```

- [ ] `7hacxjZlOZV8gdtVvyj_ow` — Bäckerei-Konditorei Stocker — Weinbergstrasse 93, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "7hacxjZlOZV8gdtVvyj_ow",
    "businessname": "Bäckerei-Konditorei Stocker",
    "address": "Weinbergstrasse 93, 8006 Zürich"
  }
  JSON
  ```

- [ ] `sQYdgeu7YSlAUAA8auhTCg` — Restaurant Dorflinde — Schwamendingenstrasse 37, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sQYdgeu7YSlAUAA8auhTCg",
    "businessname": "Restaurant Dorflinde",
    "address": "Schwamendingenstrasse 37, 8050 Zürich"
  }
  JSON
  ```

- [ ] `MOBT_12YTde-9GicMA-IWw` — Pizzeria Furetto — Wallisellenstrasse 5, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "MOBT_12YTde-9GicMA-IWw",
    "businessname": "Pizzeria Furetto",
    "address": "Wallisellenstrasse 5, 8050 Zürich"
  }
  JSON
  ```

- [ ] `v0JEaAX5m4PoQ7D8rnE0eA` — MediterRana — Albisstrasse 81, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "v0JEaAX5m4PoQ7D8rnE0eA",
    "businessname": "MediterRana",
    "address": "Albisstrasse 81, 8038 Zürich"
  }
  JSON
  ```

- [ ] `k7WemTP31nUCgR6kWPv-cw` — dean & david  franchise GmbH — Ernst-Nobs-Platz 1, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "k7WemTP31nUCgR6kWPv-cw",
    "businessname": "dean & david  franchise GmbH",
    "address": "Ernst-Nobs-Platz 1, 8004 Zürich"
  }
  JSON
  ```

- [ ] `yDB5wcMCCjh8CghjYFy0AQ` — Restaurant Weisses Kreuz — Falkenstrasse 27, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yDB5wcMCCjh8CghjYFy0AQ",
    "businessname": "Restaurant Weisses Kreuz",
    "address": "Falkenstrasse 27, 8008 Zürich"
  }
  JSON
  ```

- [ ] `b54pGs6KtRKt9aq-JyAoKA` — Restaurant Sorrento — Forchstrasse 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "b54pGs6KtRKt9aq-JyAoKA",
    "businessname": "Restaurant Sorrento",
    "address": "Forchstrasse 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `w_oVNai7R2xqIzf_si3IUw` — Chez Oskar - Bowls & Sandwiches — Hohlstrasse 485, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "w_oVNai7R2xqIzf_si3IUw",
    "businessname": "Chez Oskar - Bowls & Sandwiches",
    "address": "Hohlstrasse 485, 8048 Zürich"
  }
  JSON
  ```

- [ ] `-mr-VmD5Gx36ZCiMqotBvw` — Domino's Pizza — Hohlstrasse 502, 8048 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-mr-VmD5Gx36ZCiMqotBvw",
    "businessname": "Domino's Pizza",
    "address": "Hohlstrasse 502, 8048 Zürich"
  }
  JSON
  ```

- [ ] `e4ssBg5MxW6AUSSQ28A4tA` — Olif Restaurant — Langstrasse 81, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "e4ssBg5MxW6AUSSQ28A4tA",
    "businessname": "Olif Restaurant",
    "address": "Langstrasse 81, 8004 Zürich"
  }
  JSON
  ```

- [ ] `EhMFl031wt0vWXot6o40Vg` — Confiseur Bachmann AG — Kalanderplatz 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EhMFl031wt0vWXot6o40Vg",
    "businessname": "Confiseur Bachmann AG",
    "address": "Kalanderplatz 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `b4BY5xsWWAn0gWZRrACCvQ` — El Mechoui — Niederdorfstrasse 31, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "b4BY5xsWWAn0gWZRrACCvQ",
    "businessname": "El Mechoui",
    "address": "Niederdorfstrasse 31, 8001 Zürich"
  }
  JSON
  ```

- [ ] `q8w4hBx-lBRXgiOxLk-KRQ` — maritza — Schaffhauserstrasse 473, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "q8w4hBx-lBRXgiOxLk-KRQ",
    "businessname": "maritza",
    "address": "Schaffhauserstrasse 473, 8052 Zürich"
  }
  JSON
  ```

- [ ] `X-T3GWFwaZL-DIaQly5tHg` — Rheinfelder Bierhaus — Marktgasse 19, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "X-T3GWFwaZL-DIaQly5tHg",
    "businessname": "Rheinfelder Bierhaus",
    "address": "Marktgasse 19, 8001 Zürich"
  }
  JSON
  ```

- [ ] `J-2QaxP7j1GtLdYO-pAGyg` — La Taqueria — Badenerstrasse 138, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "J-2QaxP7j1GtLdYO-pAGyg",
    "businessname": "La Taqueria",
    "address": "Badenerstrasse 138, 8004 Zürich"
  }
  JSON
  ```

- [ ] `01lRRd9d8Q9dmAbFEUlgNQ` — Zum Husli — Risweg 1, 8041 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "01lRRd9d8Q9dmAbFEUlgNQ",
    "businessname": "Zum Husli",
    "address": "Risweg 1, 8041 Zürich"
  }
  JSON
  ```

- [ ] `THJw27Fe662BGQOEbbZ-6w` — Petite Madinina — Leutschenbachstrasse 52, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "THJw27Fe662BGQOEbbZ-6w",
    "businessname": "Petite Madinina",
    "address": "Leutschenbachstrasse 52, 8050 Zürich"
  }
  JSON
  ```

- [ ] `liL5SaNEYzIEFY5mRGsJpw` — Pizzeria La Rustica — Schaffhauserstrasse 453, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "liL5SaNEYzIEFY5mRGsJpw",
    "businessname": "Pizzeria La Rustica",
    "address": "Schaffhauserstrasse 453, 8052 Zürich"
  }
  JSON
  ```

- [ ] `eCl-bjY6i-VfRquHVVhMRA` — Hirschen — Niederdorfstrasse 13, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "eCl-bjY6i-VfRquHVVhMRA",
    "businessname": "Hirschen",
    "address": "Niederdorfstrasse 13, 8001 Zürich"
  }
  JSON
  ```

- [ ] `fh09cdkBX6YLU_FZzS82mg` — Saftlade — Münstergasse 31, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fh09cdkBX6YLU_FZzS82mg",
    "businessname": "Saftlade",
    "address": "Münstergasse 31, 8001 Zürich"
  }
  JSON
  ```

- [ ] `W0RKoHJvV5dXLkgMzUwymw` — Cooperativo, Coopi — St. Jakobstrasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "W0RKoHJvV5dXLkgMzUwymw",
    "businessname": "Cooperativo, Coopi",
    "address": "St. Jakobstrasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `CNN8y_TwuPxUQ6LMd03PFg` — Ristorante Pizzeria Chianalea — Brauerstrasse 87, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CNN8y_TwuPxUQ6LMd03PFg",
    "businessname": "Ristorante Pizzeria Chianalea",
    "address": "Brauerstrasse 87, 8004 Zürich"
  }
  JSON
  ```

- [ ] `sr7ybMsthgTWKfjzfteUpQ` — Starbucks — Limmatquai 144, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sr7ybMsthgTWKfjzfteUpQ",
    "businessname": "Starbucks",
    "address": "Limmatquai 144, 8001 Zürich"
  }
  JSON
  ```

- [ ] `FJ-tf9pzs5aXAWLzbQ8kXQ` — Shiso Burger Zurich — Weite Gasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FJ-tf9pzs5aXAWLzbQ8kXQ",
    "businessname": "Shiso Burger Zurich",
    "address": "Weite Gasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `fkDtptO9al5rsFUlsoI5JQ` — Restaurant Blume — Winterthurerstrasse 534, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fkDtptO9al5rsFUlsoI5JQ",
    "businessname": "Restaurant Blume",
    "address": "Winterthurerstrasse 534, 8051 Zürich"
  }
  JSON
  ```

- [ ] `8LLcPkq0kcN4nC12m4SbnQ` — Pizza Bonjour — Hagenholzstrasse 102, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8LLcPkq0kcN4nC12m4SbnQ",
    "businessname": "Pizza Bonjour",
    "address": "Hagenholzstrasse 102, 8050 Zürich"
  }
  JSON
  ```

- [ ] `OlH-v9sR2in6sYBSqh2cNQ` — Osteria Sazio — Seefeldstrasse 27, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OlH-v9sR2in6sYBSqh2cNQ",
    "businessname": "Osteria Sazio",
    "address": "Seefeldstrasse 27, 8008 Zürich"
  }
  JSON
  ```

- [ ] `qQ0SdAnVQpuSxctiDRqCsA` — DANTE a Bar and a Basement — Zwinglistrasse 22, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qQ0SdAnVQpuSxctiDRqCsA",
    "businessname": "DANTE a Bar and a Basement",
    "address": "Zwinglistrasse 22, 8004 Zürich"
  }
  JSON
  ```

- [ ] `_-uRjVZkC1rA0OxxTj8axA` — The Sacred mit Vegelateria — Muellerstrasse 64, 8004 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_-uRjVZkC1rA0OxxTj8axA",
    "businessname": "The Sacred mit Vegelateria",
    "address": "Muellerstrasse 64, 8004 Zürich"
  }
  JSON
  ```

- [ ] `2QS9vfiIUjCoGsBZuhA-WQ` — Zum weissen Kreuz — Rössligasse 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2QS9vfiIUjCoGsBZuhA-WQ",
    "businessname": "Zum weissen Kreuz",
    "address": "Rössligasse 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gTS4YA7fac0_boDpeEZ3gQ` — Mövenpick Wein Schweiz AG — 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gTS4YA7fac0_boDpeEZ3gQ",
    "businessname": "Mövenpick Wein Schweiz AG",
    "address": "8001 Zürich"
  }
  JSON
  ```

- [ ] `RM4CcKCVOnwkMldQqlIXLQ` — SUBWAY Restaurant — Stauffacherstrasse 101, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RM4CcKCVOnwkMldQqlIXLQ",
    "businessname": "SUBWAY Restaurant",
    "address": "Stauffacherstrasse 101, 8004 Zürich"
  }
  JSON
  ```

- [ ] `dHOH14CGXit1j0Gh0Hzb4A` — Goodys Smashburger — Mühlegasse 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dHOH14CGXit1j0Gh0Hzb4A",
    "businessname": "Goodys Smashburger",
    "address": "Mühlegasse 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `cF0xQzL7CGZ06-_nK88ioA` — HongKong Food Paradise — Kalandergasse 4, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cF0xQzL7CGZ06-_nK88ioA",
    "businessname": "HongKong Food Paradise",
    "address": "Kalandergasse 4, 8045 Zürich"
  }
  JSON
  ```

- [ ] `y6BDupfg5irv2aM7Wwsg6w` — Wirtschaft zur Au — Manessestrasse 208, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "y6BDupfg5irv2aM7Wwsg6w",
    "businessname": "Wirtschaft zur Au",
    "address": "Manessestrasse 208, 8045 Zürich"
  }
  JSON
  ```

- [ ] `ESsvxXUypeXDO-EQD4jORw` — Restaurant Café Zähringer Genossenschaft — Zähringerplatz 11, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ESsvxXUypeXDO-EQD4jORw",
    "businessname": "Restaurant Café Zähringer Genossenschaft",
    "address": "Zähringerplatz 11, 8001 Zürich"
  }
  JSON
  ```

- [ ] `BacaAY0glq9dcJgzEYb7LQ` — dieci Pizza Kurier Binz-Wollishofen — Eibenstrasse 24, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "BacaAY0glq9dcJgzEYb7LQ",
    "businessname": "dieci Pizza Kurier Binz-Wollishofen",
    "address": "Eibenstrasse 24, 8045 Zürich"
  }
  JSON
  ```

- [ ] `dptXvHaycuaQQqxg9mSnbw` — Spanische Weinhalle — Münstergasse 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dptXvHaycuaQQqxg9mSnbw",
    "businessname": "Spanische Weinhalle",
    "address": "Münstergasse 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `jQ85miH0_IOakyYWtMK6UA` — Store Central — Limmatquai 144, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jQ85miH0_IOakyYWtMK6UA",
    "businessname": "Store Central",
    "address": "Limmatquai 144, 8001 Zürich"
  }
  JSON
  ```

- [ ] `35Cn3GgynZxLRvf-SEHDdA` — Weinbistro Karim — Zwinglistrasse 6, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "35Cn3GgynZxLRvf-SEHDdA",
    "businessname": "Weinbistro Karim",
    "address": "Zwinglistrasse 6, 8004 Zürich"
  }
  JSON
  ```

- [ ] `DmvzYOhlPjegI0rNYWhK3A` — Lindas Paradise — Zähringerstrasse 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DmvzYOhlPjegI0rNYWhK3A",
    "businessname": "Lindas Paradise",
    "address": "Zähringerstrasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `pQM2ERptv2mPKtfP7_oKtg` — Simon's Steakhouse Grill & Restaurant & Bar — Niederdorfstrasse 11, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pQM2ERptv2mPKtfP7_oKtg",
    "businessname": "Simon's Steakhouse Grill & Restaurant & Bar",
    "address": "Niederdorfstrasse 11, 8001 Zürich"
  }
  JSON
  ```

- [ ] `e25ogdxkYgLPC8NFxo7NVA` — Bierwerk Züri — Gustav-Gull-Platz 10, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "e25ogdxkYgLPC8NFxo7NVA",
    "businessname": "Bierwerk Züri",
    "address": "Gustav-Gull-Platz 10, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nmmHoc55M-NODuMhntUC1A` — Pizzeria Don Emillio — Dübendorfstrasse 24, 8051 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nmmHoc55M-NODuMhntUC1A",
    "businessname": "Pizzeria Don Emillio",
    "address": "Dübendorfstrasse 24, 8051 Zürich"
  }
  JSON
  ```

- [ ] `E-pGwVN236f7fC57O-41BA` — Restaurant Opera — Dufourstrasse 2, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "E-pGwVN236f7fC57O-41BA",
    "businessname": "Restaurant Opera",
    "address": "Dufourstrasse 2, 8008 Zürich"
  }
  JSON
  ```

- [ ] `QLisN8ev675ufvogaD1nOg` — Weinstube Limmathof — Limmatquai 142, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "QLisN8ev675ufvogaD1nOg",
    "businessname": "Weinstube Limmathof",
    "address": "Limmatquai 142, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HCGWamtmdToVFzJ2HY7hFw` — Napoli da Gerardo — Sandstrasse 7, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HCGWamtmdToVFzJ2HY7hFw",
    "businessname": "Napoli da Gerardo",
    "address": "Sandstrasse 7, 8003 Zürich"
  }
  JSON
  ```

- [ ] `fXabBZwZIhTj4SI7DioJMg` — Restaurant IKOO — Bäckerstrasse 37, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fXabBZwZIhTj4SI7DioJMg",
    "businessname": "Restaurant IKOO",
    "address": "Bäckerstrasse 37, 8004 Zürich"
  }
  JSON
  ```

- [ ] `gwJmJzSB9P2mELuxxcTGog` — Bonnie Prince Pub — Zähringerstrasse 38, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gwJmJzSB9P2mELuxxcTGog",
    "businessname": "Bonnie Prince Pub",
    "address": "Zähringerstrasse 38, 8001 Zürich"
  }
  JSON
  ```

- [ ] `_6jAA4yIPQxpMvfA2UdkZw` — Äss-Bar — Stüssihofstatt 6, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_6jAA4yIPQxpMvfA2UdkZw",
    "businessname": "Äss-Bar",
    "address": "Stüssihofstatt 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `zT15jcX4liDKdeem0ee9Ag` — Gelati Tellhof — Tellstrasse 20, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "zT15jcX4liDKdeem0ee9Ag",
    "businessname": "Gelati Tellhof",
    "address": "Tellstrasse 20, 8004 Zürich"
  }
  JSON
  ```

- [ ] `3q1qNKXcrs2PKZmQoEMwCg` — Backhuus Fischer — Schaffhauserstrasse 520, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3q1qNKXcrs2PKZmQoEMwCg",
    "businessname": "Backhuus Fischer",
    "address": "Schaffhauserstrasse 520, 8052 Zürich"
  }
  JSON
  ```

- [ ] `4ZQ57Cr1L9Y89iWbo6aAvQ` — Gelati am See — Seefeldquai, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4ZQ57Cr1L9Y89iWbo6aAvQ",
    "businessname": "Gelati am See",
    "address": "Seefeldquai, 8008 Zürich"
  }
  JSON
  ```

- [ ] `XhLc5Wr6_SKTQ0yBncgBNw` — Starbucks — Europaallee 7, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XhLc5Wr6_SKTQ0yBncgBNw",
    "businessname": "Starbucks",
    "address": "Europaallee 7, 8004 Zürich"
  }
  JSON
  ```

- [ ] `L3_GfzNEreadDUM7gS2pkg` — Bank — Molkenstrasse 15, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "L3_GfzNEreadDUM7gS2pkg",
    "businessname": "Bank",
    "address": "Molkenstrasse 15, 8004 Zürich"
  }
  JSON
  ```

- [ ] `bI2vbX0Hi7mIW-j_CDHXog` — Omnia Coffee — Stauffacherstrasse 105, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "bI2vbX0Hi7mIW-j_CDHXog",
    "businessname": "Omnia Coffee",
    "address": "Stauffacherstrasse 105, 8004 Zürich"
  }
  JSON
  ```

- [ ] `XnFFGMKCMki0MuSrRMG-Pw` — L'ADORO Restaurant — Glatttalstrasse 104, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XnFFGMKCMki0MuSrRMG-Pw",
    "businessname": "L'ADORO Restaurant",
    "address": "Glatttalstrasse 104, 8052 Zürich"
  }
  JSON
  ```

- [ ] `RmAEiKqczgx-pseRuGU1Aw` — Walliser Keller im Niederdorf — Zähringerstrasse 21, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RmAEiKqczgx-pseRuGU1Aw",
    "businessname": "Walliser Keller im Niederdorf",
    "address": "Zähringerstrasse 21, 8001 Zürich"
  }
  JSON
  ```

- [ ] `IfBIs3dFe-g3zDlVeX0-uA` — La Penisola — Uetlibergstrasse 132, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IfBIs3dFe-g3zDlVeX0-uA",
    "businessname": "La Penisola",
    "address": "Uetlibergstrasse 132, 8045 Zürich"
  }
  JSON
  ```

- [ ] `AZSwcx4ebNCJ5jFtMSjm3A` — Nooch Asian Kitchen Zürich Steinfels — Heinrichstrasse 267, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AZSwcx4ebNCJ5jFtMSjm3A",
    "businessname": "Nooch Asian Kitchen Zürich Steinfels",
    "address": "Heinrichstrasse 267, 8005 Zürich"
  }
  JSON
  ```

- [ ] `5gbR7h-hfAX6t8823IllHA` — Ristorante Conti — Dufourstrasse 1, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5gbR7h-hfAX6t8823IllHA",
    "businessname": "Ristorante Conti",
    "address": "Dufourstrasse 1, 8008 Zürich"
  }
  JSON
  ```

- [ ] `D3CCwLrDitYBjWIgHWtTzg` — Dieci gelato e caffè Limmatquai — Limmatquai 32, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "D3CCwLrDitYBjWIgHWtTzg",
    "businessname": "Dieci gelato e caffè Limmatquai",
    "address": "Limmatquai 32, 8001 Zürich"
  }
  JSON
  ```

- [ ] `sqPUq08Rj18m4Up2Om__kA` — Joe & The Juice — Limmatquai 70, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sqPUq08Rj18m4Up2Om__kA",
    "businessname": "Joe & The Juice",
    "address": "Limmatquai 70, 8001 Zürich"
  }
  JSON
  ```

- [ ] `b_Bevyz30YPcarOQclU72g` — Le Chef Metas Restaurant — Kanonengasse 29, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "b_Bevyz30YPcarOQclU72g",
    "businessname": "Le Chef Metas Restaurant",
    "address": "Kanonengasse 29, 8004 Zürich"
  }
  JSON
  ```

- [ ] `xN8F1GIdWUS4EID4S8HBRg` — Veltlinerkeller (ZURICH) — Schlüsselgasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xN8F1GIdWUS4EID4S8HBRg",
    "businessname": "Veltlinerkeller (ZURICH)",
    "address": "Schlüsselgasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `lV5wxKJNP9rqM0yz2MoXqg` — Café Piazza — Idaplatz 2, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lV5wxKJNP9rqM0yz2MoXqg",
    "businessname": "Café Piazza",
    "address": "Idaplatz 2, 8003 Zürich"
  }
  JSON
  ```

- [ ] `C7CZHZxUqaADytceMBul2Q` — Steakhouse Meat Me — Rebgasse 8, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "C7CZHZxUqaADytceMBul2Q",
    "businessname": "Steakhouse Meat Me",
    "address": "Rebgasse 8, 8004 Zürich"
  }
  JSON
  ```

- [ ] `FbZ5bKOU8_Cflkes02SnYQ` — Kentucky Fried Chicken — Zürich Flughafen 3, 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FbZ5bKOU8_Cflkes02SnYQ",
    "businessname": "Kentucky Fried Chicken",
    "address": "Zürich Flughafen 3, 8060 Zürich"
  }
  JSON
  ```

- [ ] `FpnIr6F92594C1Ex4vphTA` — Châlet Suisse — 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FpnIr6F92594C1Ex4vphTA",
    "businessname": "Châlet Suisse",
    "address": "8060 Zürich"
  }
  JSON
  ```

- [ ] `W8gOPa6iyAVEGZUNaY0Jnw` — Marche Bistro — 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "W8gOPa6iyAVEGZUNaY0Jnw",
    "businessname": "Marche Bistro",
    "address": "8060 Zürich"
  }
  JSON
  ```

- [ ] `CFZFwgZexEHz2453doREow` — yámas gastro ag — Lagerstrasse 47, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CFZFwgZexEHz2453doREow",
    "businessname": "yámas gastro ag",
    "address": "Lagerstrasse 47, 8004 Zürich"
  }
  JSON
  ```

- [ ] `v8QDcGIcLo8eJnF0ElP3dQ` — Pizzeria Bella Napoli Zürich — Birmensdorferstrasse 249, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "v8QDcGIcLo8eJnF0ElP3dQ",
    "businessname": "Pizzeria Bella Napoli Zürich",
    "address": "Birmensdorferstrasse 249, 8055 Zürich"
  }
  JSON
  ```

- [ ] `MgXZogLxptV6b1Oj0jNpKg` — Casa Gourmet GmbH — Birmensdorferstrasse 259, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "MgXZogLxptV6b1Oj0jNpKg",
    "businessname": "Casa Gourmet GmbH",
    "address": "Birmensdorferstrasse 259, 8055 Zürich"
  }
  JSON
  ```

- [ ] `EY4n01GZRAdhX8LkkBMeXw` — Papa Joe's — Schifflände 18, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EY4n01GZRAdhX8LkkBMeXw",
    "businessname": "Papa Joe's",
    "address": "Schifflände 18, 8001 Zürich"
  }
  JSON
  ```

- [ ] `gzqOIwxuof-6ldUTerTPcw` — Beetnut Operations AG — Lagerstrasse 16b, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gzqOIwxuof-6ldUTerTPcw",
    "businessname": "Beetnut Operations AG",
    "address": "Lagerstrasse 16b, 8004 Zürich"
  }
  JSON
  ```

- [ ] `JuFXj4vGu5So98GSD9kfEg` — Gate Gourmet — 8058 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JuFXj4vGu5So98GSD9kfEg",
    "businessname": "Gate Gourmet",
    "address": "8058 Zürich"
  }
  JSON
  ```

- [ ] `JUu_JaKK1GL8r3qShs6kTg` — Ruen Thai By Suthita — General-Wille-Strasse 18, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JUu_JaKK1GL8r3qShs6kTg",
    "businessname": "Ruen Thai By Suthita",
    "address": "General-Wille-Strasse 18, 8002 Zürich"
  }
  JSON
  ```

- [ ] `LexZN_zctbFU-SJEo5Zl1A` — Gasthaus ZUM GUTEN GLÜCK — Stationsstrasse 7, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "LexZN_zctbFU-SJEo5Zl1A",
    "businessname": "Gasthaus ZUM GUTEN GLÜCK",
    "address": "Stationsstrasse 7, 8003 Zürich"
  }
  JSON
  ```

- [ ] `X_OwTCne0l--KKVf6sfMew` — La Pinseria — Hardplatz 9, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "X_OwTCne0l--KKVf6sfMew",
    "businessname": "La Pinseria",
    "address": "Hardplatz 9, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Qgd87S9TFN68lmPd7kFTLg` — McDonald's Restaurant — Badenerstrasse 21, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Qgd87S9TFN68lmPd7kFTLg",
    "businessname": "McDonald's Restaurant",
    "address": "Badenerstrasse 21, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Hczwpv0u-apSyhxdXMOkUQ` — Jeunesse — Wehntalerstrasse 120, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Hczwpv0u-apSyhxdXMOkUQ",
    "businessname": "Jeunesse",
    "address": "Wehntalerstrasse 120, 8057 Zürich"
  }
  JSON
  ```

- [ ] `pOrZfkR6XM8-ZoXYg3IJuw` — Tune In — Döltschiweg 234, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pOrZfkR6XM8-ZoXYg3IJuw",
    "businessname": "Tune In",
    "address": "Döltschiweg 234, 8055 Zürich"
  }
  JSON
  ```

- [ ] `aF-xIUpHgSOsoRM-QA73hw` — New Point — Albisriederplatz 5, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "aF-xIUpHgSOsoRM-QA73hw",
    "businessname": "New Point",
    "address": "Albisriederplatz 5, 8004 Zürich"
  }
  JSON
  ```

- [ ] `fBI93egKuJ_plJhNSSc1nw` — Bohemia — Klosbachstrasse 2, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fBI93egKuJ_plJhNSSc1nw",
    "businessname": "Bohemia",
    "address": "Klosbachstrasse 2, 8032 Zürich"
  }
  JSON
  ```

- [ ] `VqRtTg_SUB1xm9SINulerw` — Dal Sardo — Asylstrasse 60, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VqRtTg_SUB1xm9SINulerw",
    "businessname": "Dal Sardo",
    "address": "Asylstrasse 60, 8032 Zürich"
  }
  JSON
  ```

- [ ] `yQv0ny5ERRAsqz5dFt-kGQ` — Barfly'z — Gotthardstrasse 21, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yQv0ny5ERRAsqz5dFt-kGQ",
    "businessname": "Barfly'z",
    "address": "Gotthardstrasse 21, 8002 Zürich"
  }
  JSON
  ```

- [ ] `2iRYw6szGFEZWlVXMRfsDw` — Vier Linden — Freiestrasse 50, 8032 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2iRYw6szGFEZWlVXMRfsDw",
    "businessname": "Vier Linden",
    "address": "Freiestrasse 50, 8032 Zürich"
  }
  JSON
  ```

- [ ] `8fvrePtd-W_OAA2y1d_HWQ` — Caffe Spettacolo — Tessinerplatz 10, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8fvrePtd-W_OAA2y1d_HWQ",
    "businessname": "Caffe Spettacolo",
    "address": "Tessinerplatz 10, 8002 Zürich"
  }
  JSON
  ```

- [ ] `1u0DEdHCWJbWfMbo93mxIg` — Miss Miu — Badenerstrasse 97, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "1u0DEdHCWJbWfMbo93mxIg",
    "businessname": "Miss Miu",
    "address": "Badenerstrasse 97, 8004 Zürich"
  }
  JSON
  ```

- [ ] `xs2Tm_3Px0TMsvP2bai-pA` — Confiserie St. Jakob — Badenerstrasse 41, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xs2Tm_3Px0TMsvP2bai-pA",
    "businessname": "Confiserie St. Jakob",
    "address": "Badenerstrasse 41, 8004 Zürich"
  }
  JSON
  ```

- [ ] `yMhDKQ7Pmpv_HTay8Mvdbg` — Püente — Baumgasse 10, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yMhDKQ7Pmpv_HTay8Mvdbg",
    "businessname": "Püente",
    "address": "Baumgasse 10, 8005 Zürich"
  }
  JSON
  ```

- [ ] `N7ysflZdO8oRE3s-158bzg` — Tacos Ramiro Y Macario — Hardstrasse 9, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "N7ysflZdO8oRE3s-158bzg",
    "businessname": "Tacos Ramiro Y Macario",
    "address": "Hardstrasse 9, 8004 Zürich"
  }
  JSON
  ```

- [ ] `A00OhenWd_Z5RWnxDE7mqA` — localsearch (Swisscom Directories AG) — Förrlibuckstrasse 62, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "A00OhenWd_Z5RWnxDE7mqA",
    "businessname": "localsearch (Swisscom Directories AG)",
    "address": "Förrlibuckstrasse 62, 8005 Zürich"
  }
  JSON
  ```

- [ ] `M0BX41dEKt8oefn5GkNSgA` — Casa Ferlin AG1 — Förrlibuckstrasse 62, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "M0BX41dEKt8oefn5GkNSgA",
    "businessname": "Casa Ferlin AG1",
    "address": "Förrlibuckstrasse 62, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Y_ylXDLP3fiaZvkHtYuV2A` — Yalla Habibi — Meinrad-Lienert-Strasse 27, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Y_ylXDLP3fiaZvkHtYuV2A",
    "businessname": "Yalla Habibi",
    "address": "Meinrad-Lienert-Strasse 27, 8003 Zürich"
  }
  JSON
  ```

- [ ] `yjUfGZW0D27lU7Pdt6b6Gw` — Burgermeister Limmatplatz — Langstrasse 243, 80 05 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "yjUfGZW0D27lU7Pdt6b6Gw",
    "businessname": "Burgermeister Limmatplatz",
    "address": "Langstrasse 243, 80 05 Zürich"
  }
  JSON
  ```

- [ ] `CmaTmK9uMGD5vTXQf19Cxw` — The Vault Wine Bar — Döltschiweg 234, 8055 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CmaTmK9uMGD5vTXQf19Cxw",
    "businessname": "The Vault Wine Bar",
    "address": "Döltschiweg 234, 8055 Zürich"
  }
  JSON
  ```

- [ ] `VCYgt4-B32_Hb3QLmh9aRw` — Corner 48 — Stampfenbachplatz 4, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VCYgt4-B32_Hb3QLmh9aRw",
    "businessname": "Corner 48",
    "address": "Stampfenbachplatz 4, 8006 Zürich"
  }
  JSON
  ```

- [ ] `MR8B573IhpYDZhdd5DrM9g` — Café Bar Nordbrücke — Dammstrasse 58, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "MR8B573IhpYDZhdd5DrM9g",
    "businessname": "Café Bar Nordbrücke",
    "address": "Dammstrasse 58, 8037 Zürich"
  }
  JSON
  ```

- [ ] `TcCrSabId9XT6V22KOCuLg` — Restaurant Damas — Josefstrasse 151, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "TcCrSabId9XT6V22KOCuLg",
    "businessname": "Restaurant Damas",
    "address": "Josefstrasse 151, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Z-D1vZEcSaBB95yG1u3nXw` — Zest of Asia — Luisenstrasse 43, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Z-D1vZEcSaBB95yG1u3nXw",
    "businessname": "Zest of Asia",
    "address": "Luisenstrasse 43, 8005 Zürich"
  }
  JSON
  ```

- [ ] `kzbJPQ9e-B17iVoope_F2w` — SelnauWok GmbH — Selnaustrasse 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kzbJPQ9e-B17iVoope_F2w",
    "businessname": "SelnauWok GmbH",
    "address": "Selnaustrasse 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `upjFSyGdQNfwQbz71rQ4SA` — Residenz Restaurant — Spirgartenstrasse 2, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "upjFSyGdQNfwQbz71rQ4SA",
    "businessname": "Residenz Restaurant",
    "address": "Spirgartenstrasse 2, 8048 Zürich"
  }
  JSON
  ```

- [ ] `crORKanLMxXtanFeK8MakA` — Takano City — Löwenstrasse 29, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "crORKanLMxXtanFeK8MakA",
    "businessname": "Takano City",
    "address": "Löwenstrasse 29, 8001 Zürich"
  }
  JSON
  ```

- [ ] `EXh8YX7qKq-_J2cfUnDv6g` — Sorell Hotel Seidenhof — Sihlstrasse 9, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EXh8YX7qKq-_J2cfUnDv6g",
    "businessname": "Sorell Hotel Seidenhof",
    "address": "Sihlstrasse 9, 8001 Zürich"
  }
  JSON
  ```

- [ ] `AYJfVHKxzPuJ4hbZ6p8tYQ` — Rice Up! Stadelhofen — Stadelhoferstrasse 18, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AYJfVHKxzPuJ4hbZ6p8tYQ",
    "businessname": "Rice Up! Stadelhofen",
    "address": "Stadelhoferstrasse 18, 8001 Zürich"
  }
  JSON
  ```

- [ ] `aJVsNPZorsROvZ9jHFXV4Q` — Edomae — Talstrasse 62, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "aJVsNPZorsROvZ9jHFXV4Q",
    "businessname": "Edomae",
    "address": "Talstrasse 62, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Pxc2twCUsZFjDXPT-jlJVg` — azzurri — Badenerstrasse, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Pxc2twCUsZFjDXPT-jlJVg",
    "businessname": "azzurri",
    "address": "Badenerstrasse, 8048 Zürich"
  }
  JSON
  ```

- [ ] `2wBHGPU6qpSfRwgD0ywBaw` — Original Kebap House — Franklinstrasse 20, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "2wBHGPU6qpSfRwgD0ywBaw",
    "businessname": "Original Kebap House",
    "address": "Franklinstrasse 20, 8050 Zürich"
  }
  JSON
  ```

- [ ] `ZhKyqPZi3Be-3Q0HVb449w` — dieci Pizza Kurier Zürichberg — Landoltstrasse 7, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZhKyqPZi3Be-3Q0HVb449w",
    "businessname": "dieci Pizza Kurier Zürichberg",
    "address": "Landoltstrasse 7, 8006 Zürich"
  }
  JSON
  ```

- [ ] `fECzgCHCby0yAay7n0fc8g` — Best Kebab — Langstrasse 206, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fECzgCHCby0yAay7n0fc8g",
    "businessname": "Best Kebab",
    "address": "Langstrasse 206, 8005 Zürich"
  }
  JSON
  ```

- [ ] `KrNyru4gx4RAuozpHf23jA` — Emma's Bakery — Schaffhauserstrasse 125, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KrNyru4gx4RAuozpHf23jA",
    "businessname": "Emma's Bakery",
    "address": "Schaffhauserstrasse 125, 8057 Zürich"
  }
  JSON
  ```

- [ ] `ve1094FSlT8PCZbLrFtb1Q` — Rest. Kornhaus — Langstrasse 243, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ve1094FSlT8PCZbLrFtb1Q",
    "businessname": "Rest. Kornhaus",
    "address": "Langstrasse 243, 8005 Zürich"
  }
  JSON
  ```

- [ ] `eKkt6ycatSv5r5NlTWnkQw` — Famiglia Tremonte — Birmensdorferstrasse 129, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "eKkt6ycatSv5r5NlTWnkQw",
    "businessname": "Famiglia Tremonte",
    "address": "Birmensdorferstrasse 129, 8003 Zürich"
  }
  JSON
  ```

- [ ] `gAVeB2esapc9QShAV6IIZw` — Restaurant & Pizzeria da Angelo — Badenerstrasse 275, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "gAVeB2esapc9QShAV6IIZw",
    "businessname": "Restaurant & Pizzeria da Angelo",
    "address": "Badenerstrasse 275, 8003 Zürich"
  }
  JSON
  ```

- [ ] `3lLSAV26ZQunER0HNjL3UQ` — Walhalla Hotel — Limmatstrasse 5, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3lLSAV26ZQunER0HNjL3UQ",
    "businessname": "Walhalla Hotel",
    "address": "Limmatstrasse 5, 8005 Zürich"
  }
  JSON
  ```

- [ ] `GQZtd69tqdnhrc0_GYJdpA` — Brasserie Spirgarten — Lindenplatz 5, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GQZtd69tqdnhrc0_GYJdpA",
    "businessname": "Brasserie Spirgarten",
    "address": "Lindenplatz 5, 8048 Zürich"
  }
  JSON
  ```

- [ ] `DYoDvMx8Dhh4mjTab5v1TQ` — First Base Afrofood — Badenerstrasse 276, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DYoDvMx8Dhh4mjTab5v1TQ",
    "businessname": "First Base Afrofood",
    "address": "Badenerstrasse 276, 8004 Zürich"
  }
  JSON
  ```

- [ ] `DB6A3EY7fxk3y670buc2og` — Nadas — Bederstrasse 77, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DB6A3EY7fxk3y670buc2og",
    "businessname": "Nadas",
    "address": "Bederstrasse 77, 8002 Zürich"
  }
  JSON
  ```

- [ ] `-5O2nEiAxGiAVphjOH7ZSA` — Kian — Stampfenbachstrasse 24, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-5O2nEiAxGiAVphjOH7ZSA",
    "businessname": "Kian",
    "address": "Stampfenbachstrasse 24, 8001 Zürich"
  }
  JSON
  ```

- [ ] `b9feuEikUQmFIU7MLR8a1Q` — Il Baretto Josef — Josefstrasse 13, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "b9feuEikUQmFIU7MLR8a1Q",
    "businessname": "Il Baretto Josef",
    "address": "Josefstrasse 13, 8005 Zürich"
  }
  JSON
  ```

- [ ] `WGZV3glDJp1BKZUzy4CAyA` — Micas Garten — Badenerstrasse 790, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "WGZV3glDJp1BKZUzy4CAyA",
    "businessname": "Micas Garten",
    "address": "Badenerstrasse 790, 8048 Zürich"
  }
  JSON
  ```

- [ ] `RzF8WsDlBxgtl4nBRNSCwg` — Restaurant TESSIN GROTTO — Waidbadstrasse 151, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "RzF8WsDlBxgtl4nBRNSCwg",
    "businessname": "Restaurant TESSIN GROTTO",
    "address": "Waidbadstrasse 151, 8037 Zürich"
  }
  JSON
  ```

- [ ] `qgR4s1g_F-zs_CjCP7vi_w` — Swiss Bistro — Schiffbaustrasse 11, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qgR4s1g_F-zs_CjCP7vi_w",
    "businessname": "Swiss Bistro",
    "address": "Schiffbaustrasse 11, 8005 Zürich"
  }
  JSON
  ```

- [ ] `cSfn_ZAcycAebg_c6m4yLg` — Commihalles — Stampfenbachstrasse 6, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cSfn_ZAcycAebg_c6m4yLg",
    "businessname": "Commihalles",
    "address": "Stampfenbachstrasse 6, 8001 Zürich"
  }
  JSON
  ```

- [ ] `e0vtQ7bTtXsVIP3-7Z9IFw` — Burger Brothers GmbH — Altstetterstrasse 147, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "e0vtQ7bTtXsVIP3-7Z9IFw",
    "businessname": "Burger Brothers GmbH",
    "address": "Altstetterstrasse 147, 8048 Zürich"
  }
  JSON
  ```

- [ ] `fj7DXO926W8woe3yS6MvkQ` — Marktlücke GmbH — Hermetschloostrasse 70, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fj7DXO926W8woe3yS6MvkQ",
    "businessname": "Marktlücke GmbH",
    "address": "Hermetschloostrasse 70, 8048 Zürich"
  }
  JSON
  ```

- [ ] `M1oSki-mzf9tFQesNwcl6w` — Thai Sun Garden — Winterthurerstrasse 281, 8057 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "M1oSki-mzf9tFQesNwcl6w",
    "businessname": "Thai Sun Garden",
    "address": "Winterthurerstrasse 281, 8057 Zürich"
  }
  JSON
  ```

- [ ] `rHMNSf83nrncw9VvRKcPhg` — BARADOX — Sihlstrasse 73, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rHMNSf83nrncw9VvRKcPhg",
    "businessname": "BARADOX",
    "address": "Sihlstrasse 73, 8001 Zürich"
  }
  JSON
  ```

- [ ] `5Zj9hWF1kzdPJz-RjaiHxw` — Venice Bar — Schiffbaustrasse 4, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "5Zj9hWF1kzdPJz-RjaiHxw",
    "businessname": "Venice Bar",
    "address": "Schiffbaustrasse 4, 8005 Zürich"
  }
  JSON
  ```

- [ ] `oGcoSoh6VKsOdNZLmHBHNQ` — FAMO — Talstrasse 20, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "oGcoSoh6VKsOdNZLmHBHNQ",
    "businessname": "FAMO",
    "address": "Talstrasse 20, 8001 Zürich"
  }
  JSON
  ```

- [ ] `JdN2Fgsg3L_LLlysFzh4xg` — The Counter — Bahnhofplatz 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "JdN2Fgsg3L_LLlysFzh4xg",
    "businessname": "The Counter",
    "address": "Bahnhofplatz 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `CgLebB9HJKgnBMj-WAchww` — Caredda Paolo — Josefstrasse 119, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CgLebB9HJKgnBMj-WAchww",
    "businessname": "Caredda Paolo",
    "address": "Josefstrasse 119, 8005 Zürich"
  }
  JSON
  ```

- [ ] `aQFj6FZ0lVMKO4rZc54NuA` — Kaimug Altstetten — Altstetterstrasse 145, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "aQFj6FZ0lVMKO4rZc54NuA",
    "businessname": "Kaimug Altstetten",
    "address": "Altstetterstrasse 145, 8048 Zürich"
  }
  JSON
  ```

- [ ] `lhILKmVD0vadCBAVD3Si0A` — Walliser Kanne — Lintheschergasse 21, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lhILKmVD0vadCBAVD3Si0A",
    "businessname": "Walliser Kanne",
    "address": "Lintheschergasse 21, 8001 Zürich"
  }
  JSON
  ```

- [ ] `fPAZBNzBQnCzM3yPd_2_Pw` — Ristorante Toscano Im Puls 5 — Giessereistrasse 18, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fPAZBNzBQnCzM3yPd_2_Pw",
    "businessname": "Ristorante Toscano Im Puls 5",
    "address": "Giessereistrasse 18, 8005 Zürich"
  }
  JSON
  ```

- [ ] `s1AVBrtUScVJYoIOMq7OMw` — Restaurant La Terrasse — Badenerstrasse 537, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "s1AVBrtUScVJYoIOMq7OMw",
    "businessname": "Restaurant La Terrasse",
    "address": "Badenerstrasse 537, 8048 Zürich"
  }
  JSON
  ```

- [ ] `cVkcY-NwfGtw-rxMqkZX_Q` — Grottino 83 — Letzigraben 245, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cVkcY-NwfGtw-rxMqkZX_Q",
    "businessname": "Grottino 83",
    "address": "Letzigraben 245, 8047 Zürich"
  }
  JSON
  ```

- [ ] `saNqgMgsJMJCr8ekMsCjqg` — Felix — Kalkbreitestrasse 8, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "saNqgMgsJMJCr8ekMsCjqg",
    "businessname": "Felix",
    "address": "Kalkbreitestrasse 8, 8003 Zürich"
  }
  JSON
  ```

- [ ] `XaFc3_6wiFYrcPHLNdK2qw` — Restaurant Schützenruh AG — Uetlibergstrasse 300, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XaFc3_6wiFYrcPHLNdK2qw",
    "businessname": "Restaurant Schützenruh AG",
    "address": "Uetlibergstrasse 300, 8045 Zürich"
  }
  JSON
  ```

- [ ] `Sk8YpPfHXre9i_RZxYyloA` — Gastrolac Resto GmbH — Seestrasse 495, 8038 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Sk8YpPfHXre9i_RZxYyloA",
    "businessname": "Gastrolac Resto GmbH",
    "address": "Seestrasse 495, 8038 Zürich"
  }
  JSON
  ```

- [ ] `Fdk-tdjPb91hA6slsv-cqw` — China Restaurant — Tessinerplatz 12, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Fdk-tdjPb91hA6slsv-cqw",
    "businessname": "China Restaurant",
    "address": "Tessinerplatz 12, 8002 Zürich"
  }
  JSON
  ```

- [ ] `31lzOvK_ _8nVc1PQNGaxpA` — Da Pizzi — Josefstrasse 27, 8005 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "31lzOvK_ _8nVc1PQNGaxpA",
    "businessname": "Da Pizzi",
    "address": "Josefstrasse 27, 8005 Zürich"
  }
  JSON
  ```

- [ ] `GCsfT-eoUU2G4FOiRmLAHg` — FiveSpice Thai Restaurant — Zweierstrasse 106, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GCsfT-eoUU2G4FOiRmLAHg",
    "businessname": "FiveSpice Thai Restaurant",
    "address": "Zweierstrasse 106, 8003 Zürich"
  }
  JSON
  ```

- [ ] `vrJIe9DWBPatVM0uFt5joA` — Restaurant AXOi — Meinrad-Lienert-Strasse 23, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vrJIe9DWBPatVM0uFt5joA",
    "businessname": "Restaurant AXOi",
    "address": "Meinrad-Lienert-Strasse 23, 8003 Zürich"
  }
  JSON
  ```

- [ ] `Y45CYqVkUy2awmjj3ZHBaQ` — HUA THAI — Hardstrasse 320, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Y45CYqVkUy2awmjj3ZHBaQ",
    "businessname": "HUA THAI",
    "address": "Hardstrasse 320, 8005 Zürich"
  }
  JSON
  ```

- [ ] `_TT36JeTjIAzvoEe81mnBA` — Zumfondue — Museumstrasse 1, 8001 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "_TT36JeTjIAzvoEe81mnBA",
    "businessname": "Zumfondue",
    "address": "Museumstrasse 1, 8001 Zürich"
  }
  JSON
  ```

- [ ] `6lt5x50m1TUn-elWEgCNsw` — Cafeteria KS Stadelhofen — Promenadengasse 5, 8090 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "6lt5x50m1TUn-elWEgCNsw",
    "businessname": "Cafeteria KS Stadelhofen",
    "address": "Promenadengasse 5, 8090 Zürich"
  }
  JSON
  ```

- [ ] `LTUcznib4XbdYeZ95N-pGw` — Osteria da Biagio — Limmattalstrasse 228, 8049 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "LTUcznib4XbdYeZ95N-pGw",
    "businessname": "Osteria da Biagio",
    "address": "Limmattalstrasse 228, 8049 Zürich"
  }
  JSON
  ```

- [ ] `KTEXUS_xsKDGY1LFrMqO1A` — Osteria Centrale — Nordstrasse 205, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KTEXUS_xsKDGY1LFrMqO1A",
    "businessname": "Osteria Centrale",
    "address": "Nordstrasse 205, 8037 Zürich"
  }
  JSON
  ```

- [ ] `ZnwJMgWfiZhaTsuUJ-zeIA` — Le Jardin — Stockerstrasse 17, 8002 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ZnwJMgWfiZhaTsuUJ-zeIA",
    "businessname": "Le Jardin",
    "address": "Stockerstrasse 17, 8002 Zürich"
  }
  JSON
  ```

- [ ] `kiY78SwOqmqPLQlfgKAyMA` — Nagasui AG — Selnaustrasse 16, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "kiY78SwOqmqPLQlfgKAyMA",
    "businessname": "Nagasui AG",
    "address": "Selnaustrasse 16, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Slla1mzF6sr7UH5HucQeYQ` — Pret A Manger Dock D — Postfach 2472, Bahnhofsterminal, Zürich Flughafen, 8060 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Slla1mzF6sr7UH5HucQeYQ",
    "businessname": "Pret A Manger Dock D",
    "address": "Postfach 2472, Bahnhofsterminal, Zürich Flughafen, 8060 Zürich"
  }
  JSON
  ```

- [ ] `3PHK62yE89D9oIPEHMCfqA` — 'itos — Neymarstrasse 25, 8311 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "3PHK62yE89D9oIPEHMCfqA",
    "businessname": "'itos",
    "address": "Neymarstrasse 25, 8311 Zürich"
  }
  JSON
  ```

- [ ] `vHL2TbutZ4U3wn_nuOfd8g` — Restaurant La Côte — Aemtlerstrasse 26, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vHL2TbutZ4U3wn_nuOfd8g",
    "businessname": "Restaurant La Côte",
    "address": "Aemtlerstrasse 26, 8003 Zürich"
  }
  JSON
  ```

- [ ] `f3hKW0EULE8ixrM1MQPL4A` — Cafeteria ZHdK Sihlquai — Sihlquai 87, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "f3hKW0EULE8ixrM1MQPL4A",
    "businessname": "Cafeteria ZHdK Sihlquai",
    "address": "Sihlquai 87, 8005 Zürich"
  }
  JSON
  ```

- [ ] `xDpY3FN3pv7_uC4TVMBUjA` — EQUINOX Restaurant — Turbinenstrasse 20, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xDpY3FN3pv7_uC4TVMBUjA",
    "businessname": "EQUINOX Restaurant",
    "address": "Turbinenstrasse 20, 8005 Zürich"
  }
  JSON
  ```

- [ ] `363f7XDw8zWJ-ZrfAwoVcw` — Restauarant Grotto Reale — Martastrasse 145, 8003 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "363f7XDw8zWJ-ZrfAwoVcw",
    "businessname": "Restauarant Grotto Reale",
    "address": "Martastrasse 145, 8003 Zürich"
  }
  JSON
  ```

- [ ] `fNopuqCM3E7eQs1QoSjm6Q` — Frau Gerolds Garten — Geroldstrasse 23A, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fNopuqCM3E7eQs1QoSjm6Q",
    "businessname": "Frau Gerolds Garten",
    "address": "Geroldstrasse 23A, 8005 Zürich"
  }
  JSON
  ```

- [ ] `KTJg0pSXKWObC6qEptxFrQ` — Burgermeister — Hardstrasse 316, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KTJg0pSXKWObC6qEptxFrQ",
    "businessname": "Burgermeister",
    "address": "Hardstrasse 316, 8005 Zürich"
  }
  JSON
  ```

- [ ] `P1wwhkZR7aRcYdA1xsPnrA` — Steiner Flughafebeck — Turbinenstrasse 22, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "P1wwhkZR7aRcYdA1xsPnrA",
    "businessname": "Steiner Flughafebeck",
    "address": "Turbinenstrasse 22, 8005 Zürich"
  }
  JSON
  ```

- [ ] `0FKms4RRfO5ZsVx187xENw` — Old Fashion Bar AG — Fraumünsterstrasse 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0FKms4RRfO5ZsVx187xENw",
    "businessname": "Old Fashion Bar AG",
    "address": "Fraumünsterstrasse 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `rhoUejeL6HaKAAo490R3HA` — Vis à Vis — Talstrasse 40, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "rhoUejeL6HaKAAo490R3HA",
    "businessname": "Vis à Vis",
    "address": "Talstrasse 40, 8001 Zürich"
  }
  JSON
  ```

- [ ] `dTMPpeLQLuNSA1JcYWu2yg` — Kai Sushi Schiffbau Zürich — Hardstrasse 261, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "dTMPpeLQLuNSA1JcYWu2yg",
    "businessname": "Kai Sushi Schiffbau Zürich",
    "address": "Hardstrasse 261, 8005 Zürich"
  }
  JSON
  ```

- [ ] `Rvb8eYY6z9gBkdOqrG85Fg` — La Pizza Buona — Altstetterstrasse 239, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Rvb8eYY6z9gBkdOqrG85Fg",
    "businessname": "La Pizza Buona",
    "address": "Altstetterstrasse 239, 8048 Zürich"
  }
  JSON
  ```

- [ ] `VsUDF2vHreQEtErzBaI5WQ` — SUC+ Juice Bars — 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VsUDF2vHreQEtErzBaI5WQ",
    "businessname": "SUC+ Juice Bars",
    "address": "8050 Zürich"
  }
  JSON
  ```

- [ ] `qavb0cROXgYAN5Virf9PHw` — Restaurant Löwen Siam — Baumackerstrasse 47, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qavb0cROXgYAN5Virf9PHw",
    "businessname": "Restaurant Löwen Siam",
    "address": "Baumackerstrasse 47, 8050 Zürich"
  }
  JSON
  ```

- [ ] `VO6cOzcmf8GuACroVp_pBg` — Restaurant Sonne Libanon — Altstetterstrasse 223, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VO6cOzcmf8GuACroVp_pBg",
    "businessname": "Restaurant Sonne Libanon",
    "address": "Altstetterstrasse 223, 8048 Zürich"
  }
  JSON
  ```

- [ ] `CAQdmfSmTPcUjCPpVBO9wg` — ATELIER BAR — Talacker 16, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CAQdmfSmTPcUjCPpVBO9wg",
    "businessname": "ATELIER BAR",
    "address": "Talacker 16, 8001 Zürich"
  }
  JSON
  ```

- [ ] `0jL2QzXFj6y8KeVlQMTszw` — McDonald's Restaurant — Hofwiesenstrasse 350-354, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "0jL2QzXFj6y8KeVlQMTszw",
    "businessname": "McDonald's Restaurant",
    "address": "Hofwiesenstrasse 350-354, 8050 Zürich"
  }
  JSON
  ```

- [ ] `jKzC1Qed4kQ5DZZzxZT9WA` — SAIGON — Sihlstrasse 97, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "jKzC1Qed4kQ5DZZzxZT9WA",
    "businessname": "SAIGON",
    "address": "Sihlstrasse 97, 8001 Zürich"
  }
  JSON
  ```

- [ ] `renz3HWMUycJbXa9tcHU6w` — Bärengasse Restaurant — Bahnhofstrasse 25, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "renz3HWMUycJbXa9tcHU6w",
    "businessname": "Bärengasse Restaurant",
    "address": "Bahnhofstrasse 25, 8001 Zürich"
  }
  JSON
  ```

- [ ] `T-JSe1kssU6N8CmLH9D6HA` — Ayverdi's Oerlikon — Genossenschaftsstrasse 18, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "T-JSe1kssU6N8CmLH9D6HA",
    "businessname": "Ayverdi's Oerlikon",
    "address": "Genossenschaftsstrasse 18, 8050 Zürich"
  }
  JSON
  ```

- [ ] `DgRbhGxaIrrFrIn1u50bsg` — Williams ButchersTable Hegibachplatz — Neumünsterstrasse 34, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DgRbhGxaIrrFrIn1u50bsg",
    "businessname": "Williams ButchersTable Hegibachplatz",
    "address": "Neumünsterstrasse 34, 8008 Zürich"
  }
  JSON
  ```

- [ ] `UXn6QLTrCIcW_kkdgogboA` — Fusio — Max-Bill-Platz 15, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "UXn6QLTrCIcW_kkdgogboA",
    "businessname": "Fusio",
    "address": "Max-Bill-Platz 15, 8050 Zürich"
  }
  JSON
  ```

- [ ] `Tkcw2Nr8vlV0N-BQCM3rcQ` — Ristorante Da Angela — Hohlstrasse 449, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Tkcw2Nr8vlV0N-BQCM3rcQ",
    "businessname": "Ristorante Da Angela",
    "address": "Hohlstrasse 449, 8048 Zürich"
  }
  JSON
  ```

- [ ] `y1rEUgTbk9VyjlntEZKWGQ` — Brasserie La Pontaise — Krönleinstrasse 14, 8044 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "y1rEUgTbk9VyjlntEZKWGQ",
    "businessname": "Brasserie La Pontaise",
    "address": "Krönleinstrasse 14, 8044 Zürich"
  }
  JSON
  ```

- [ ] `IuSbePwsucAjJ4RnVclTBg` — Samurai VII — Badenerstrasse 651, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "IuSbePwsucAjJ4RnVclTBg",
    "businessname": "Samurai VII",
    "address": "Badenerstrasse 651, 8048 Zürich"
  }
  JSON
  ```

- [ ] `T81EQsKXtNmqEtoHa6ux9A` — eCHo — Neumühlequai 42, 8006 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "T81EQsKXtNmqEtoHa6ux9A",
    "businessname": "eCHo",
    "address": "Neumühlequai 42, 8006 Zürich"
  }
  JSON
  ```

- [ ] `ii-kdnOaA2h40KaVlxAuFQ` — McDonald's Restaurant — Hohlstrasse 467, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ii-kdnOaA2h40KaVlxAuFQ",
    "businessname": "McDonald's Restaurant",
    "address": "Hohlstrasse 467, 8048 Zürich"
  }
  JSON
  ```

- [ ] `HBg9EuSq2GFomwFrbelXKw` — Hotel Glockenhof — Sihlstrasse 31, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HBg9EuSq2GFomwFrbelXKw",
    "businessname": "Hotel Glockenhof",
    "address": "Sihlstrasse 31, 8001 Zürich"
  }
  JSON
  ```

- [ ] `20WIKrwBt2Rlu1J1XsHErw` — tibits — Tramstrasse 2, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "20WIKrwBt2Rlu1J1XsHErw",
    "businessname": "tibits",
    "address": "Tramstrasse 2, 8050 Zürich"
  }
  JSON
  ```

- [ ] `qLynStOJF6sC0F0ARLrFQw` — Backerei Hug — Vulkanplatz 31, 8048 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qLynStOJF6sC0F0ARLrFQw",
    "businessname": "Backerei Hug",
    "address": "Vulkanplatz 31, 8048 Zürich"
  }
  JSON
  ```

- [ ] `ruS3buwBHFCWjdUcAQmgCg` — AURA Group AG — Bleicherweg 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ruS3buwBHFCWjdUcAQmgCg",
    "businessname": "AURA Group AG",
    "address": "Bleicherweg 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `FHKO0L40ZXm_JSHux5-4jw` — Café du Bonheur GmbH — Zypressenstrasse 115, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FHKO0L40ZXm_JSHux5-4jw",
    "businessname": "Café du Bonheur GmbH",
    "address": "Zypressenstrasse 115, 8004 Zürich"
  }
  JSON
  ```

- [ ] `VQ7LWGF9Uk4scSHnczoJMA` — Restaurant Börni's Baizli — Tramstrasse 17, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VQ7LWGF9Uk4scSHnczoJMA",
    "businessname": "Restaurant Börni's Baizli",
    "address": "Tramstrasse 17, 8050 Zürich"
  }
  JSON
  ```

- [ ] `-sEHa5O0kT8zvPrJhZHjyA` — Letzistübli — Albisriederstrasse 171, 8047 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-sEHa5O0kT8zvPrJhZHjyA",
    "businessname": "Letzistübli",
    "address": "Albisriederstrasse 171, 8047 Zürich"
  }
  JSON
  ```

- [ ] `E7mGnVU3wfRoxUrZv48fyg` — Nikos Griechische Taverne — A lbisriederstrasse 181, 8047 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "E7mGnVU3wfRoxUrZv48fyg",
    "businessname": "Nikos Griechische Taverne",
    "address": "A lbisriederstrasse 181, 8047 Zürich"
  }
  JSON
  ```

- [ ] `WTW_Ra_l0GfINlQ9lLoVvQ` — 50zu5 — Zollikerstrasse 6, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "WTW_Ra_l0GfINlQ9lLoVvQ",
    "businessname": "50zu5",
    "address": "Zollikerstrasse 6, 8008 Zürich"
  }
  JSON
  ```

- [ ] `lLl1wRlxvqDUOz4sOywVlw` — LOFT FIVE — Europaallee 15, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "lLl1wRlxvqDUOz4sOywVlw",
    "businessname": "LOFT FIVE",
    "address": "Europaallee 15, 8004 Zürich"
  }
  JSON
  ```

- [ ] `-nATy3Z3uJl_Zoek70nOwQ` — Spuntino — Bellerivestrasse 253, 8008 Zürich
  - **Warning:** The source `entry_id` begins with or contains unsupported whitespace/punctuation. The API is expected to reject it; the value is preserved exactly for correction.

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "-nATy3Z3uJl_Zoek70nOwQ",
    "businessname": "Spuntino",
    "address": "Bellerivestrasse 253, 8008 Zürich"
  }
  JSON
  ```

- [ ] `AK_7BgSvo5jYS3rSy70qHA` — Rheinfelder Bierhalle — Niederdorfstrasse 76, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "AK_7BgSvo5jYS3rSy70qHA",
    "businessname": "Rheinfelder Bierhalle",
    "address": "Niederdorfstrasse 76, 8001 Zürich"
  }
  JSON
  ```

- [ ] `51YVzr4DcPydBphOaeRUIw` — Convivio — Rotwandstrasse 62, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "51YVzr4DcPydBphOaeRUIw",
    "businessname": "Convivio",
    "address": "Rotwandstrasse 62, 8004 Zürich"
  }
  JSON
  ```

- [ ] `NN-796mIiF4JvvkbyiTEHQ` — Restaurant Tüfenegg — Dufourstrasse 154, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "NN-796mIiF4JvvkbyiTEHQ",
    "businessname": "Restaurant Tüfenegg",
    "address": "Dufourstrasse 154, 8008 Zürich"
  }
  JSON
  ```

- [ ] `CX-H-vCICcS3uYw6XaR4ZQ` — Habesha GmbH — Schreinerstrasse 64, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CX-H-vCICcS3uYw6XaR4ZQ",
    "businessname": "Habesha GmbH",
    "address": "Schreinerstrasse 64, 8004 Zürich"
  }
  JSON
  ```

- [ ] `nM6t5qipJ8Oyl85e0vgCzQ` — Brauerei Oerlikon AG — Schärenmoosstrasse 105, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "nM6t5qipJ8Oyl85e0vgCzQ",
    "businessname": "Brauerei Oerlikon AG",
    "address": "Schärenmoosstrasse 105, 8052 Zürich"
  }
  JSON
  ```

- [ ] `8Cq_bQt-BZ-IsW7dI71FnA` — Cèdre-Bellevue — Schifflände 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8Cq_bQt-BZ-IsW7dI71FnA",
    "businessname": "Cèdre-Bellevue",
    "address": "Schifflände 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `WBvoM3YGP2o12tYFzKs55w` — Vohdin Urs — Oberdorfstrasse 12, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "WBvoM3YGP2o12tYFzKs55w",
    "businessname": "Vohdin Urs",
    "address": "Oberdorfstrasse 12, 8001 Zürich"
  }
  JSON
  ```

- [ ] `GRrAvcos-I0a251z0sVYMw` — Kuhn Bäckerei Cafe — Leimbachstrasse 23, 8041 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "GRrAvcos-I0a251z0sVYMw",
    "businessname": "Kuhn Bäckerei Cafe",
    "address": "Leimbachstrasse 23, 8041 Zürich"
  }
  JSON
  ```

- [ ] `pcG1TsJuXm4TGRDw48Hzsg` — Restaurant Zeughaushof — Kanonengasse 20, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pcG1TsJuXm4TGRDw48Hzsg",
    "businessname": "Restaurant Zeughaushof",
    "address": "Kanonengasse 20, 8004 Zürich"
  }
  JSON
  ```

- [ ] `qnFV4hLSuTCwvkns2vmmxw` — Celia — Langstrasse 35, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "qnFV4hLSuTCwvkns2vmmxw",
    "businessname": "Celia",
    "address": "Langstrasse 35, 8004 Zürich"
  }
  JSON
  ```

- [ ] `ow07qLETefBX83AppgtykQ` — Restaurant Druckzentrum Bubenberg — Bubenbergstrasse 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ow07qLETefBX83AppgtykQ",
    "businessname": "Restaurant Druckzentrum Bubenberg",
    "address": "Bubenbergstrasse 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `xBuFdcWRc_zmWZQ9J2SbLw` — Pizzeria Piazza — Wehntalerstrasse 546, 8046 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xBuFdcWRc_zmWZQ9J2SbLw",
    "businessname": "Pizzeria Piazza",
    "address": "Wehntalerstrasse 546, 8046 Zürich"
  }
  JSON
  ```

- [ ] `XgTc-SuFym6jqgvXhEoXFg` — BarMünster — Münstergasse 30, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "XgTc-SuFym6jqgvXhEoXFg",
    "businessname": "BarMünster",
    "address": "Münstergasse 30, 8001 Zürich"
  }
  JSON
  ```

- [ ] `vnVHV4n8grH1HnO_WI6Pow` — Don Leone — Bäckerstrasse 31, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vnVHV4n8grH1HnO_WI6Pow",
    "businessname": "Don Leone",
    "address": "Bäckerstrasse 31, 8004 Zürich"
  }
  JSON
  ```

- [ ] `Tpt2CKmMxyU4OgEN00xIRQ` — Libanesisch Cèdre — Badenerstrasse 78, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Tpt2CKmMxyU4OgEN00xIRQ",
    "businessname": "Libanesisch Cèdre",
    "address": "Badenerstrasse 78, 8004 Zürich"
  }
  JSON
  ```

- [ ] `vgHGNt2_8JUJf0GQk8IkMA` — Masi Wine Bar & Restaurant — Seefeldstrasse 5, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "vgHGNt2_8JUJf0GQk8IkMA",
    "businessname": "Masi Wine Bar & Restaurant",
    "address": "Seefeldstrasse 5, 8008 Zürich"
  }
  JSON
  ```

- [ ] `78xMMLEcC4WtVY2byw72Pw` — Restaurant Madrid — Froschaugasse 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "78xMMLEcC4WtVY2byw72Pw",
    "businessname": "Restaurant Madrid",
    "address": "Froschaugasse 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `t3IvATLsxkeYmo7WXI_iTw` — Chinagarten Take Away — Bellerivestrasse 144, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "t3IvATLsxkeYmo7WXI_iTw",
    "businessname": "Chinagarten Take Away",
    "address": "Bellerivestrasse 144, 8008 Zürich"
  }
  JSON
  ```

- [ ] `mhDJ6LNUdEWMeshkhUPlbg` — Restaurant La Zagra — Seefeldstrasse 273, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "mhDJ6LNUdEWMeshkhUPlbg",
    "businessname": "Restaurant La Zagra",
    "address": "Seefeldstrasse 273, 8008 Zürich"
  }
  JSON
  ```

- [ ] `cv9xfPxAnHuxGyeED9VCfA` — Restaurant Bar noon — Oberdorfstrasse 9, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cv9xfPxAnHuxGyeED9VCfA",
    "businessname": "Restaurant Bar noon",
    "address": "Oberdorfstrasse 9, 8001 Zürich"
  }
  JSON
  ```

- [ ] `Ko0CiFPwkmyRNsoYh6ZQCA` — CS clube-social — Zeughaushof 3, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "Ko0CiFPwkmyRNsoYh6ZQCA",
    "businessname": "CS clube-social",
    "address": "Zeughaushof 3, 8004 Zürich"
  }
  JSON
  ```

- [ ] `8Sx24OlrJxK0ONLDEBSUKQ` — Hammam Basar AG — Mühlebachstrasse 155, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "8Sx24OlrJxK0ONLDEBSUKQ",
    "businessname": "Hammam Basar AG",
    "address": "Mühlebachstrasse 155, 8008 Zürich"
  }
  JSON
  ```

- [ ] `DC3yewmG9082XkPGiKv22A` — La Lup, Asian Kitchen — Wolframplatz 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DC3yewmG9082XkPGiKv22A",
    "businessname": "La Lup, Asian Kitchen",
    "address": "Wolframplatz 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `o0SbTqeqWnye2bWvwABtCA` — Sushi Nation — Köschenrütistrasse 6, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "o0SbTqeqWnye2bWvwABtCA",
    "businessname": "Sushi Nation",
    "address": "Köschenrütistrasse 6, 8052 Zürich"
  }
  JSON
  ```

- [ ] `djyNtpC1EsMVycK9vPsBCQ` — Cafe Kornsilo — Seefeldstrasse 231, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "djyNtpC1EsMVycK9vPsBCQ",
    "businessname": "Cafe Kornsilo",
    "address": "Seefeldstrasse 231, 8008 Zürich"
  }
  JSON
  ```

- [ ] `OgeyfaL_tPQ8bM8a8q9ExA` — Bar Zänker — Zähringerstrasse 39, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "OgeyfaL_tPQ8bM8a8q9ExA",
    "businessname": "Bar Zänker",
    "address": "Zähringerstrasse 39, 8001 Zürich"
  }
  JSON
  ```

- [ ] `cMlIMWiMXulU9vnBQ7odvw` — Zunfthaus am Neumarkt — Neumarkt 5, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "cMlIMWiMXulU9vnBQ7odvw",
    "businessname": "Zunfthaus am Neumarkt",
    "address": "Neumarkt 5, 8001 Zürich"
  }
  JSON
  ```

- [ ] `889Q66TsV6pHS3wAdpXWZA` — Landhus — Katzenbachstrasse 10, 8052 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "889Q66TsV6pHS3wAdpXWZA",
    "businessname": "Landhus",
    "address": "Katzenbachstrasse 10, 8052 Zürich"
  }
  JSON
  ```

- [ ] `4Gcr-wm8br_EG92qkZ2ZlQ` — Store Sihlcity — Kalanderplatz 1, 8045 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "4Gcr-wm8br_EG92qkZ2ZlQ",
    "businessname": "Store Sihlcity",
    "address": "Kalanderplatz 1, 8045 Zürich"
  }
  JSON
  ```

- [ ] `KPXMYH5LZSgihdo1UZ6fuQ` — Phuket Asia Center — Schöneggstrasse 21, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "KPXMYH5LZSgihdo1UZ6fuQ",
    "businessname": "Phuket Asia Center",
    "address": "Schöneggstrasse 21, 8004 Zürich"
  }
  JSON
  ```

- [ ] `xQ5piiQ5peeZxbDQxwQk7Q` — EquiTable AG — Stauffacherstrasse 163, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "xQ5piiQ5peeZxbDQxwQk7Q",
    "businessname": "EquiTable AG",
    "address": "Stauffacherstrasse 163, 8004 Zürich"
  }
  JSON
  ```

- [ ] `9OIo061XvdH0r4LmXxxqyw` — Khujug — Schöneggstrasse 5, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "9OIo061XvdH0r4LmXxxqyw",
    "businessname": "Khujug",
    "address": "Schöneggstrasse 5, 8004 Zürich"
  }
  JSON
  ```

- [ ] `pSNHIhKQobfCpYbRHGXpJA` — Maison 33 Cafe & Bistro — Höschgasse 33, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pSNHIhKQobfCpYbRHGXpJA",
    "businessname": "Maison 33 Cafe & Bistro",
    "address": "Höschgasse 33, 8008 Zürich"
  }
  JSON
  ```

- [ ] `CzZHlRmbQ0Ck5-K8jovoIA` — Raclette-Stube — Zähringerstrasse 16, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "CzZHlRmbQ0Ck5-K8jovoIA",
    "businessname": "Raclette-Stube",
    "address": "Zähringerstrasse 16, 8001 Zürich"
  }
  JSON
  ```

- [ ] `HGl8JOiGkE_U6P81GHsQww` — Wirtschaft Unterdorf — Katzenseestrasse 15, 8046 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "HGl8JOiGkE_U6P81GHsQww",
    "businessname": "Wirtschaft Unterdorf",
    "address": "Katzenseestrasse 15, 8046 Zürich"
  }
  JSON
  ```

- [ ] `ee5i63KsuwHVTYsxZkF0ug` — Bodega Española — Münstergasse 15, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "ee5i63KsuwHVTYsxZkF0ug",
    "businessname": "Bodega Española",
    "address": "Münstergasse 15, 8001 Zürich"
  }
  JSON
  ```

- [ ] `DFaH8FzqVGpXbnu1OIJKTw` — Kaffeehandel — Münstergasse 19, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "DFaH8FzqVGpXbnu1OIJKTw",
    "businessname": "Kaffeehandel",
    "address": "Münstergasse 19, 8001 Zürich"
  }
  JSON
  ```

- [ ] `v5vK1szqlL_o7RrAlCnjzg` — Tšüri Grill — Hönggerstrasse 13, 8037 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "v5vK1szqlL_o7RrAlCnjzg",
    "businessname": "Tšüri Grill",
    "address": "Hönggerstrasse 13, 8037 Zürich"
  }
  JSON
  ```

- [ ] `sJ5W3ik7dxJxaQlMSweSJQ` — Restaurant HONGXI — Zwinglistrasse 3, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "sJ5W3ik7dxJxaQlMSweSJQ",
    "businessname": "Restaurant HONGXI",
    "address": "Zwinglistrasse 3, 8004 Zürich"
  }
  JSON
  ```

- [ ] `VGIurioVsxUO5E8IegyXfw` — Zunfthaus zur Saffran — Limmatquai 54, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "VGIurioVsxUO5E8IegyXfw",
    "businessname": "Zunfthaus zur Saffran",
    "address": "Limmatquai 54, 8001 Zürich"
  }
  JSON
  ```

- [ ] `EJaiwjqTHKMPif4QKNqR5A` — 4 Tiere Bar — Feldstrasse 61, 8004 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "EJaiwjqTHKMPif4QKNqR5A",
    "businessname": "4 Tiere Bar",
    "address": "Feldstrasse 61, 8004 Zürich"
  }
  JSON
  ```

- [ ] `oAOK4w6rY4CGltD4oNCeVQ` — b.good International — Oberdorfstrasse 8, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "oAOK4w6rY4CGltD4oNCeVQ",
    "businessname": "b.good International",
    "address": "Oberdorfstrasse 8, 8001 Zürich"
  }
  JSON
  ```

- [ ] `32pNx0Nf6X1sTTgd2vAuEw` — Acasa Suites Zürich — Binzmühlestrasse 72, 8050 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "32pNx0Nf6X1sTTgd2vAuEw",
    "businessname": "Acasa Suites Zürich",
    "address": "Binzmühlestrasse 72, 8050 Zürich"
  }
  JSON
  ```

- [ ] `pohmXOz8DhG5nHneusttNg` — Pizza Nation — Rosengasse 3, 8001 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "pohmXOz8DhG5nHneusttNg",
    "businessname": "Pizza Nation",
    "address": "Rosengasse 3, 8001 Zürich"
  }
  JSON
  ```

- [ ] `fwz-yFxIGYMxCDLkue7_0g` — Ristorante Amalfi — Mainaustrasse 23, 8008 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "fwz-yFxIGYMxCDLkue7_0g",
    "businessname": "Ristorante Amalfi",
    "address": "Mainaustrasse 23, 8008 Zürich"
  }
  JSON
  ```

- [ ] `SLTAJZ8tymFJ7MGGpxus1g` — Aubrey — Schiffbaustrasse 10, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "SLTAJZ8tymFJ7MGGpxus1g",
    "businessname": "Aubrey",
    "address": "Schiffbaustrasse 10, 8005 Zürich"
  }
  JSON
  ```

- [ ] `FvSOfUv_8a1Qm5S1J44KtQ` — Noerd Kantine — Schiffbaustrasse 10, 8005 Zürich

  ```bash
  curl --fail-with-body -sS \
    -X POST http://127.0.0.1:8000/api/v1/register \
    -H 'content-type: application/json' \
    --data-binary @- <<'JSON'
  {
    "entry_id": "FvSOfUv_8a1Qm5S1J44KtQ",
    "businessname": "Noerd Kantine",
    "address": "Binzmühlestrasse 170, 8050 Zürich"
  }
  JSON
  ```