#!/usr/bin/env bash
# Register all restaurants from docs/EXAMPLES.md against the executor API.
# Generated from docs/EXAMPLES.md — regenerate rather than hand-editing entries.
#
# Run on spider-01 (the API is published on VM loopback only):
#   ./scripts/register-restaurants.sh
#
# Each request is asynchronous; the API creates or reuses the entry's Doctor
# task, so re-running the whole script is safe. A failed request does not stop
# the run; failures are summarized at the end.
set -u

API="${SPIDER_API_URL:-http://127.0.0.1:8000}"

ok=0
failed=0
failures=()

while IFS= read -r payload; do
  [ -z "$payload" ] && continue
  entry_id=$(sed -E 's/.*"entry_id": "([^"]+)".*/\1/' <<<"$payload")
  if response=$(curl --fail-with-body -sS \
      -X POST "$API/api/v1/register" \
      -H 'content-type: application/json' \
      --data-binary "$payload" </dev/null 2>&1); then
    ok=$((ok + 1))
    printf 'ok   %s\n' "$entry_id"
  else
    failed=$((failed + 1))
    failures+=("$entry_id")
    printf 'FAIL %s: %s\n' "$entry_id" "$response" >&2
  fi
done <<'ENTRIES'
{"entry_id": "Ob1139zJg0uzvHg1VlP6vA", "businessname": "DaboSmoothies", "address": "Birmensdorferstrasse 285, 8003 Zürich"}
{"entry_id": "OWjbydCNXagwj8ikDHALuw", "businessname": "Piazza", "address": "Idaplatz 2, 8003 Zürich"}
{"entry_id": "AoOkoCRZ9SAeam0tWRrOgQ", "businessname": "Donde Luis", "address": "Militärstrasse 114, 8004 Zürich"}
{"entry_id": "Jv5ZTKsgxAhxJzgfSnbFXw", "businessname": "Volkshaus", "address": "Stauffacherstrasse 60, 8004 Zürich"}
{"entry_id": "8TjEjvh9Kb6JNXnnqWYhaA", "businessname": "not guilty Airgate AG", "address": "Thurgauerstrasse 40, 8050 Zürich"}
{"entry_id": "WdIsQ0-sFvwaENPvT6N03w", "businessname": "Haue", "address": "Limmatquai 52, 8001 Zürich"}
{"entry_id": "gQwfZ_z4wwJM7_5GSXwjMA", "businessname": "Osteria Borgo", "address": "Niederdorfstrasse 33, 8001 Zürich"}
{"entry_id": "dUgMwmWlwauwgR3kL4aOug", "businessname": "Centro Lusitano de Zurique zum Hüsli", "address": "Risweg 1, 8041 Zürich"}
{"entry_id": "nDjGVaTfTILieRxg3ETaAw", "businessname": "Peking Garden China-Restaurant Take Away", "address": "Langstrasse 13, 8004 Zürich"}
{"entry_id": "0N5paWNcn0yK3FmC3DP2XA", "businessname": "Platzhirsch", "address": "Spitalgasse 3, 8001 Zürich"}
{"entry_id": "Ptqf_GdJBxjcEkJ_8uStRw", "businessname": "Mucho Gusto", "address": "Reitergasse 6, 8004 Zürich"}
{"entry_id": "MwSzyU-pjR5VxWMHNXDG4A", "businessname": "Restaurant Tschingg am Stauffacher", "address": "Lutherstrasse 4, 8004 Zürich"}
{"entry_id": "q2GV6lMpcKHv3u22Xuj2gw", "businessname": "Restaurant Lanchid", "address": "Rebgasse 8, 8004 Zürich"}
{"entry_id": "GHVj2fGdi2vI4rtS0BCsLQ", "businessname": "China Restaurant", "address": "Langstrasse 11, 8004 Zürich"}
{"entry_id": "nMtpNpUvmIAjegc2IOjbTA", "businessname": "The Studio", "address": "Dufourstrasse 23, 8008 Zürich"}
{"entry_id": "Zb-8lJ_Mx-BY8s6W8l30og", "businessname": "Bye Bye Bar", "address": "Check-in 2, Level 2, ZRH Airport, 8058 Zürich"}
{"entry_id": "9zoZ_L8Y97tluPUPAQQzSQ", "businessname": "Dolce Vita II", "address": "Häringstrasse 2, 8001 Zürich"}
{"entry_id": "rSca1EnQ1vu2YgelRgof_g", "businessname": "The News Deli", "address": "8000 Zürich"}
{"entry_id": "RB6zCB39qZBE8u-uVds_jQ", "businessname": "Ristorante Italia", "address": "Zeughausstrasse 61, 8004 Zürich"}
{"entry_id": "LxdrVU5f6eRSD_s5YbzmFw", "businessname": "Cafeteria ZHAW", "address": "Lagerstrasse 45, 8004 Zürich"}
{"entry_id": "O69Cn-gHItd_Jdy86vRAeA", "businessname": "Monocle Shop & Cafe", "address": "Dufourstrasse 90, 8008 Zürich"}
{"entry_id": "xCG0lTxFJvWtAcrutREs8w", "businessname": "Swiss Chuchi Restaurant", "address": "Rosengasse 10, 8001 Zürich"}
{"entry_id": "dwgsM2T9miPTtl8aKdxSSw", "businessname": "Brasserie Café de Paris", "address": "Ankerstrasse 113, 8004 Zürich"}
{"entry_id": "Qr1w5U2VzDj_BGGH7UZnhA", "businessname": "Restaurant Neufeld", "address": "Friesenbergstrasse 15, 8055 Zürich"}
{"entry_id": "kJFTs6JsUNLVTmUPA_gG0w", "businessname": "Aggarwal AG", "address": "Kernstrasse 27, 8004 Zürich"}
{"entry_id": "jM6PiafIt90sLJCpwu99dA", "businessname": "NENI Zürich Langstrasse", "address": "Langstrasse 150, 8004 Zürich"}
{"entry_id": "1Khw8hpB1D1xydr5-OHsew", "businessname": "Memolino", "address": "Leutschenbachstrasse 50, 8050 Zürich"}
{"entry_id": "FpQBBqbeQfs1I10w2QqHbA", "businessname": "Café Felix am Bellevue", "address": "Bellevueplatz 5, 8001 Zürich"}
{"entry_id": "L71nxPQpJZ-KHb23Sk7Z8g", "businessname": "Drinx Bar", "address": "Dufourstrasse 24, 8008 Zürich"}
{"entry_id": "AAg4H7FNsVG9NDlYaThfGg", "businessname": "Rathaus-Café", "address": "Limmatquai 61, 8001 Zürich"}
{"entry_id": "8q67s0zGC1yG-i7-jLexiQ", "businessname": "Neumärt", "address": "Neumarkt 28, 8001 Zürich"}
{"entry_id": "zl8klEdtjUgXxzoUmx7m1Q", "businessname": "Café Henrici", "address": "Niederdorfstrasse 1, 8001 Zürich"}
{"entry_id": "kfNcdso5dL3HhpI9FlTiNg", "businessname": "Asia Restaurant", "address": "8060 Zürich"}
{"entry_id": "e3F-0T3Xi13i3wbcwaW1gg", "businessname": "NEUMARKT", "address": "Neumarkt 5, 8001 Zürich"}
{"entry_id": "wFJgnSSK_mdXORsSuFU4Ow", "businessname": "Safari Bar", "address": "Zähringerstrasse 29, 8001 Zürich"}
{"entry_id": "pgqO7fOemFzKnGLypCkobA", "businessname": "ZAATAR", "address": "Brauerstrasse 74, 8004 Zürich"}
{"entry_id": "orMO22woRL6zE5HFGak_Hw", "businessname": "Jasmin", "address": "Herzogenmühlestrasse 4, 8051 Zürich"}
{"entry_id": "1EhTjvzVDTgHUOerpv4ZHA", "businessname": "Bistrot chez Marion", "address": "Mühlegasse 22, 8001 Zürich"}
{"entry_id": "yqd3PvUQPF--7_cia3ZxWw", "businessname": "Teecafe Schwarzenbach", "address": "Münstergasse 17, 8001 Zürich"}
{"entry_id": "6M-i-i4ZvORTXesE2Irrww", "businessname": "Bauernschänke", "address": "Rindermarkt 24, 8001 Zürich"}
{"entry_id": "Gir5T9vd140Qs26YPXl2gw", "businessname": "Trottoir Gastro", "address": "Schöneggstrasse 23, 8004 Zürich"}
{"entry_id": "3pCLHrmCvlIxDNQH8mhXmw", "businessname": "Hotel Neufeld", "address": "Friesenbergstrasse 15, 8055 Zürich"}
{"entry_id": "EzVN9HBKEc43JwR8JyEkDg", "businessname": "SMITH AND DE LUMA", "address": "Grubenstrasse 27, 8045 Zürich"}
{"entry_id": "x8Gsxrp9zMKTjldtpkvHgA", "businessname": "Hasta Ice Cream", "address": "Zwingliplatz 3, 8001 Zürich"}
{"entry_id": "vlP5mNW6vZeXQlQsHAmcYg", "businessname": "Piadina Bar", "address": "Niederdorfstrasse 2, 8001 Zürich"}
{"entry_id": "mosSkISHpvH3HaNwZod9BA", "businessname": "Morgenstern", "address": "Zwinglistrasse 27, 8004 Zürich"}
{"entry_id": "84xQNlPQXXYwCyV_fCr5jQ", "businessname": "Hospiz @ Gotthard Bar", "address": "Langstrasse 63, 8004 Zürich"}
{"entry_id": "3yC74CRNyazk7I3_umEFtA", "businessname": "dean & david ZH Wiesenstrasse", "address": "Wiesenstrasse 1, 8008 Zürich"}
{"entry_id": "7ozC0bhN9BOLeU-mjrbQSQ", "businessname": "Burgermeister", "address": "Langstrasse 6, 8004 Zürich"}
{"entry_id": "LFUZkOdEC_1D8Z7cjRzg0A", "businessname": "Capri Pizzeria", "address": "Dufourstrasse 80, 8008 Zürich"}
{"entry_id": "ueGQLQqfvqdhFZyYS9e6qA", "businessname": "Restaurant Commercio", "address": "Mühlebachstrasse 2, 8008 Zürich"}
{"entry_id": "7LY0U5jTCWP1zYMddSAbFQ", "businessname": "King Rice Restaurant", "address": "Schaffhauserstrasse 413, 8050 Zürich"}
{"entry_id": "eFWTFtYlE6c7xxlAb6tM3g", "businessname": "Griechische Taverne L & P GmbH", "address": "Seefeldstrasse 167, 8008 Zürich"}
{"entry_id": "rX-BqCmt6l4X7fcdNMKnLw", "businessname": "Dialog", "address": "Münstergasse 4, 8001 Zürich"}
{"entry_id": "gfYcLy5JbtPiUQKRBImiNw", "businessname": "Exer Gastronomie GmbH", "address": "Tellstrasse 10, 8004 Zürich"}
{"entry_id": "v4Vc7DJWoQxqwAXgOjHYMg", "businessname": "Giusi's Ristorante Pizzeria", "address": "Zollikerstrasse 10, 8008 Zürich"}
{"entry_id": "oAoHm28TDCi_o4zTIPzung", "businessname": "Restaurant Schlüssel", "address": "Seefeldstrasse 177, 8008 Zürich"}
{"entry_id": "AagN-fnvVURHzWaVxadp2Q", "businessname": "Restaurant/Take Away Tschingg Oberdorf", "address": "Oberdorfstrasse 2, 8001 Zürich"}
{"entry_id": "N-cXLa7bitDFMl6bsrv6AQ", "businessname": "Blaue Ente", "address": "Seefeldstrasse 223, 8008 Zürich"}
{"entry_id": "RImoJQPF5SaOy0zfA6A1yw", "businessname": "Payamlino Take Away", "address": "Uetlibergstrasse 103, 8045 Zürich"}
{"entry_id": "E-kt3FQx08WrWfY4D-CHRA", "businessname": "Kafi Mümpfeli", "address": "Wehntalerstrasse 286, 8046 Zürich"}
{"entry_id": "5DfzfI3OUGzBz05d0uHOxA", "businessname": "Petra's Tip-Top-Bar", "address": "Seilergraben 13, 8001 Zürich"}
{"entry_id": "CTERGmSvrYyANpVumRreqA", "businessname": "PLOY THAI RESTAURANT HONGBIN", "address": "Uetlibergstrasse 38, 8045 Zürich"}
{"entry_id": "8bMWNcOZlAGPPUkO9Lhj-w", "businessname": "UBS Restaurant Europaallee", "address": "Eisgasse 10, 8004 Zürich"}
{"entry_id": "u7GvyqIiO4EJzstcvfY05A", "businessname": "Weinschenke Hotel Hirschen", "address": "Hirschengasse, 8001 Zürich"}
{"entry_id": "DPaObTzZjYC16zvtRT48DQ", "businessname": "BACKbAR", "address": "Seefeldstrasse 169, 8008 Zürich"}
{"entry_id": "Z74C2bLqcnEf5-UoFzOR7g", "businessname": "Accademia Del Gusto", "address": "Rotwandstrasse 48, 8004 Zürich"}
{"entry_id": "nPY8QiOx6XYk7awkdvBPjA", "businessname": "f39 restaurant", "address": "Fröhlichstrasse 39, 8008 Zürich"}
{"entry_id": "GvAUCMu6sNPf23wAIa87_w", "businessname": "Restaurant Johanniter", "address": "Niederdorfstrasse 70, 8001 Zürich"}
{"entry_id": "HsWouR3P0-dM4u3UtgvTmg", "businessname": "Itasia", "address": "Dufourstrasse 57, 8008 Zürich"}
{"entry_id": "IOWTFtTJe_ZkJqSHgL0R9g", "businessname": "Bar Andorra", "address": "Münstergasse 20, 8001 Zürich"}
{"entry_id": "5GBj0ilLYS2VFIC3ylpNIg", "businessname": "Gasthaus Albisgütli", "address": "Uetlibergstrasse 341, 8045 Zürich"}
{"businessname": "Restaurant Eichhörnli", "entry_id": "MdCuSADh178WWHMeO8rFgw", "address": "Nietengasse 16, 8004 Zürich"}
{"entry_id": "e-OyP8BuRHWa_uFZnWx10Q", "businessname": "Ban Song Thai", "address": "Kirchgasse 6, 8001 Zürich"}
{"entry_id": "PA6qRaKHs613yybiVaaTrw", "businessname": "Angels Wine Tower Grill", "address": "8058 Zürich"}
{"entry_id": "tBy5dc1yhXwSlwq1v218AQ", "businessname": "Burger King", "address": "8060 Zürich"}
{"entry_id": "3TNm6avPCTluuq9WWQNBOQ", "businessname": "Pret A Manger Dock E", "address": "8060 Zürich"}
{"entry_id": "0Z780hMbIiDCtI4asiUOcA", "businessname": "Sablier - Rooftop Restaurant & Bar", "address": "The Circle 23, 8058 Zürich"}
{"entry_id": "U14r22WSEiXw8DyuwCMdag", "businessname": "HSV Clubhaus - Der Dorf Treffpunkt", "address": "Hagenholzstrasse 81a, 8050 Zürich"}
{"entry_id": "MBX6whPF3HxlNwzdQ149WQ", "businessname": "Avenida", "address": "Strassburgstrasse 17, 8004 Zürich"}
{"entry_id": "lKrPrkJYEfrfXYikXM0IzA", "businessname": "Babi's Bagel Shop", "address": "Bederstrasse 102, 8002 Zürich"}
{"entry_id": "JVe1KJ6OE_cO_6AtuU6cPQ", "businessname": "Flussbad Unterer Letten", "address": "Wasserwerkstrasse 131, 8037 Zürich"}
{"entry_id": "0dmLcpHNerR8vnrHFRoxTQ", "businessname": "Cafe Presse Club", "address": "Münsterhof 15, 8001 Zürich"}
{"entry_id": "G7Fc4ytLyBoDSypUO6P1Jw", "businessname": "Maison Blunt", "address": "Gasometerstrasse 5, 8005 Zürich"}
{"entry_id": "uklnRySCO-Ny0--0R1Qi1w", "businessname": "Restaurant UniTurm", "address": "Rämistrasse 71, 8006 Zürich"}
{"entry_id": "IcpUePMDANvvBJYRSlIr0Q", "businessname": "Riviera Pizzeria", "address": "Förrlibuckstrasse 62, 8005 Zürich"}
{"entry_id": "sdKK4aYfa5vaW82Vo5mS4Q", "businessname": "Seerestaurant Badi Wollishofen", "address": "Seestrasse 451, 8038 Zürich"}
{"entry_id": "kZzNzNAQk4RNLaiXizre3w", "businessname": "Restaurant Markthalle", "address": "Limmatstrasse 231, 8005 Zürich"}
{"entry_id": "rLyoGfhM5NM0drHXrmSQ9Q", "businessname": "Kailash Parbat", "address": "Claridenstrasse 36, 8002 Zürich"}
{"entry_id": "tu-L0BB8ci03-jF74IqGIQ", "businessname": "Vivid Tapas Bar", "address": "Turbinenstrasse 20, 8005 Zürich"}
{"entry_id": "nOrmUgn0CexqiVfwq6pcJA", "businessname": "O'Callaghan's Shamrock Pub", "address": "Studackerstrasse 1, 8038 Zürich"}
{"entry_id": "I5QK2jj8qQbfqfMsts11nA", "businessname": "RAW by Michael Adams", "address": "Ackerstrasse 56, 8005 Zürich"}
{"entry_id": "DoKUXpc7zHomXPxvHN6t5g", "businessname": "Restaurant Am Brühlbach", "address": "Kappenbühlweg 11, 8049 Zürich"}
{"entry_id": "2vqwOYl3jaOuV1bHFmomJQ", "businessname": "Devi Deli Göttlich Vegan", "address": "Bertastrasse 11, 8003 Zürich"}
{"entry_id": "FhL_m63EYtSnSEQfSzJqtw", "businessname": "Mercure Hotel Stoller Zürich", "address": "Badenerstrasse 357, 8003 Zürich"}
{"entry_id": "VXHbU99j5ci8v4iY3qQYyA", "businessname": "Il Pantheon", "address": "Limmattalstrasse 400, 8049 Zürich"}
{"entry_id": "kNu1IG-2OZV_zI2Z3ypQaA", "businessname": "Billiardino", "address": "Heinrichstrasse 245, 8005 Zürich"}
{"entry_id": "u_aMz7r27vS7QrtMJj3Ppw", "businessname": "Wesley's Kitchen", "address": "8001 Zürich"}
{"entry_id": "r7BdEQ1dyS9j2CSp6Hhs_w", "businessname": "Babo's Restaurant", "address": "Langstrasse 192, 8005 Zürich"}
{"entry_id": "dq43HWfMEJPDSH-R7eaO7w", "businessname": "Zest of Asia", "address": "Luisenstrasse 43, 8005 Zürich"}
{"entry_id": "HJZuur1BKpgniXIU5LbtYw", "businessname": "Restaurant Yan-Ruyi", "address": "Albisstrasse 19, 8038 Zürich"}
{"entry_id": "7MuWaGquV3CCK9ODPFldmQ", "businessname": "Thali House Indian Restaurant", "address": "Langstrasse 213, 8005 Zürich"}
{"entry_id": "RP7addpBrHPOJczUzOYvkA", "businessname": "The Lemon Grass Thai Take Away & Catering", "address": "Limmatstrasse 199, 8005 Zürich"}
{"entry_id": "Gu1VJWFRJ3ivHDiBYJ89TA", "businessname": "Pizzeria Antonio", "address": "Hardturmstrasse 133, 8005 Zürich"}
{"entry_id": "YNIuUXqIpI3BJQAX6GcqxQ", "businessname": "Noona", "address": "Albisstrasse 107, 8038 Zürich"}
{"entry_id": "Xq--O7RXbpPJH5Fhu_DOIg", "businessname": "ONA POKÉ AG", "address": "Lintheschergasse 13, 8001 Zürich"}
{"entry_id": "DsGXp4OnbN2A5S13luZP8Q", "businessname": "Café du Centenaire", "address": "Badenerstrasse 571, 8048 Zürich"}
{"entry_id": "7RKDv6WFWWNnsUYeKG2vUg", "businessname": "Magoosh Grill - Restaurant - Bar", "address": "Stampfenbachstrasse 6, 8001 Zürich"}
{"entry_id": "vO07-PdHr_vlyRPoUUHeGw", "businessname": "Fujiya of Japan", "address": "Tessinerplatz 5, 8002 Zürich"}
{"entry_id": "trU5ncCqMf8qtseYfA2v2w", "businessname": "Arogyam", "address": "Badenerstrasse 298, 8004 Zürich"}
{"entry_id": "YjVylVPPIzYb3Gszc64FtQ", "businessname": "Cucina Milchbuck", "address": "Schaffhauserstrasse 113, 8057 Zürich"}
{"entry_id": "5vX6l1QaIeaiyozekTgEdQ", "businessname": "Urban Fork", "address": "Ackerstrasse 56, 8005 Zürich"}
{"entry_id": "ckuetyLZQJfhfF45W0s7_g", "businessname": "Genovas Fine Food & Beverage", "address": "Bertastrasse 26, 8003 Zürich"}
{"entry_id": "-6tlhQ5q6U9tq4xVLNAIkg", "businessname": "Ristorante Italia", "address": "Witikonerstrasse 289, 8053 Zürich"}
{"entry_id": "bWkcnzb6WmG5YBMWPMkNYA", "businessname": "Café Bebek AG", "address": "Badenerstrasse 171, 8003 Zürich"}
{"entry_id": "ZolGiJcaVYAdfhA-MW-CJw", "businessname": "Quartier 5", "address": "Hardturmstrasse 126A, 8005 Zürich"}
{"entry_id": "Tibq2KtHTc0Ti1iiNjpAFA", "businessname": "Belvoirpark Restaurant", "address": "Seestrasse 125, 8002 Zürich"}
{"entry_id": "dRV7z6MMgOSBac1z3SVJpA", "businessname": "Albis Beck Café Frankental", "address": "Konrad-Ilg-Strasse 4, 8049 Zürich"}
{"entry_id": "cZr8m11TJi8M5PQGBeQhTQ", "businessname": "By Khalid Mexican Restaurant", "address": "Schaffhauserstrasse 116, 8057 Zürich"}
{"entry_id": "VqKL_iUYh9ySJc6eMQ40Zw", "businessname": "Backerei Hug", "address": "Stauffacherstrasse 28, 8004 Zürich"}
{"entry_id": "Qvhhxfj_G1aO8X1bx8W_tQ", "businessname": "Starbucks Coffee House", "address": "Limmatstrasse 5, 8005 Zürich"}
{"entry_id": "CIwgWvgGsenhtGZZucDIxA", "businessname": "Pizza Kebab Lochergut", "address": "Badenerstrasse 213, 8003 Zürich"}
{"entry_id": "uRuFyD17pCKt0C5TbT9sHg", "businessname": "3 Brüder Ristorante Pizzeria GmbH", "address": "Limmatstrasse 125, 8005 Zürich"}
{"entry_id": "B07OyPgQ9m0xT-q6_yMaCQ", "businessname": "Tadka Restaurant", "address": "Quellenstrasse 49, 8005 Zürich"}
{"entry_id": "ihvRQpopNz8RmREVl2K8oA", "businessname": "Restaurant Medina", "address": "Albisstrasse 72, 8038 Zürich"}
{"entry_id": "4XXX9RX9y_etvLg7BLFK7w", "businessname": "Fein und Schein", "address": "Schöntalstrasse 14, 8004 Zürich"}
{"entry_id": "_G66OOCKSeOjO2JWkr6aNA", "businessname": "Kulturmarkt", "address": "Aemtlerstrasse 23, 8003 Zürich"}
{"entry_id": "6tMwkhf3d0TsUzHrAhs2MQ", "businessname": "Bar Enge", "address": "Seestrasse 7, 8002 Zürich"}
{"entry_id": "krfYQCaiIOd4UDf3owHtRg", "businessname": "Burgers & Shakes", "address": "Birmensdorferstrasse 430, 8055 Zürich"}
{"entry_id": "M8NQIbdqvZQTFGFmQZOjyA", "businessname": "Hermanseck", "address": "Birmensdorferstrasse 58, 8004 Zürich"}
{"entry_id": "055jLpexaW3agQfdjrF3bQ", "businessname": "El Luchador", "address": "Konradstrasse 69, 8005 Zürich"}
{"entry_id": "HhOfN0EBw5B6zKcjrsLigg", "businessname": "Vee's Bistro", "address": "Alfred-Escher-Strasse 11, 8002 Zürich"}
{"entry_id": "6UEeG987MoId-zHEOekh-w", "businessname": "Konditorei Berner", "address": "Hottingerstrasse 33, 8032 Zürich"}
{"entry_id": "ECXCEQAr8Jectlh3bv6Emw", "businessname": "Nooba", "address": "Kreuzplatz 5, 8032 Zürich"}
{"entry_id": "OEzwTbNFoiGZXYtSLMsVLg", "businessname": "ViCOLLECTIVE AG", "address": "Zollstrasse 117, 8005 Zürich"}
{"entry_id": "ANZe4U_M5uu7FlqMQMscxg", "businessname": "Ruenthai 2 Take Away", "address": "Badenerstrasse 582, 8048 Zürich"}
{"entry_id": "-Lf_fuI1Bqq-sOFpDJNcdQ", "businessname": "Reblaube", "address": "Glockengasse 7, 8001 Zürich"}
{"entry_id": "vJU4Ynylo36in_jnsAEHvQ", "businessname": "Restaurant Bar Café Ey Hof", "address": "Triemlistrasse 183, 8047 Zürich"}
{"entry_id": "kWFxqQl8Q_nIMZZfyi7lkQ", "businessname": "Royal Panda", "address": "Forchstrasse 2, 8008 Zürich"}
{"entry_id": "i3tFjsOmQRgxOfHcavCLGw", "businessname": "Waiana Tiki Bar", "address": "Glockengasse 7, 8001 Zürich"}
{"entry_id": "gKvvfk-Oh9_KZKFaHsWM6Q", "businessname": "Läderach Chocolatier Suisse", "address": "Bahnhofstrasse 106, 8001 Zürich"}
{"entry_id": "ULVQ4eQlr8jDUTsV7umeJQ", "businessname": "Cafe Altstetten", "address": "Altstetterstrasse 130, 8048 Zürich"}
{"entry_id": "ndZWID4LZBOBVUighSd1NA", "businessname": "Bäckerei & Konditorei - Café Peter", "address": "Tramstrasse 235, 8050 Zürich"}
{"entry_id": "U4ntcBopbywljkUmckUYtQ", "businessname": "Cantinetta Antinori", "address": "Augustinergasse 25, 8001 Zürich"}
{"entry_id": "xT7HR7SUxerL2v7h_UrRVA", "businessname": "Foodpoint Restaurant", "address": "Kreuzplatz 8008, 8008 Zürich"}
{"entry_id": "ZuUbImxGu5VzqIBPaproZQ", "businessname": "Cafeteria BS für Detailhandel - Niklausstrasse", "address": "Niklausstrasse 16, 8006 Zürich"}
{"entry_id": "RsDHsOEBKgcQmuDhZ6ayBQ", "businessname": "ZAWAN Thai Kitchen", "address": "Rigiplatz 1, 8006 Zürich"}
{"entry_id": "5A-dhdQR4Tw_1vw1eXv0iw", "businessname": "Restaurant Pizza Züri", "address": "Badenerstrasse 558, 8048 Zürich"}
{"entry_id": "tcTpNO9hdh6R2-XdIoUKSQ", "businessname": "Burger King", "address": "8001 Zürich"}
{"entry_id": "VEcAPmtyf0aLs-LP_XRRBg", "businessname": "Gabbani Zürich", "address": "Talstrasse 40, 8001 Zürich"}
{"entry_id": "tzLqbCd_xSOGmC_VbGcr_w", "businessname": "Mövenpick Ice Cream Gallery", "address": "Theaterstrasse 8, 8001 Zürich"}
{"entry_id": "CB1WJYis4gm8EtlEFWmvIg", "businessname": "Ali Osman Engin", "address": "Wallisellenstrasse 5, 8050 Zürich"}
{"entry_id": "WuCiA-7Bvi25iGpGLAJqCg", "businessname": "Hiltl Akademie", "address": "Sihlstrasse 24, 8001 Zürich"}
{"entry_id": "lonh-3XCzgCii0hqIqORng", "businessname": "Konrad", "address": "Lintheschergasse 23, 8001 Zürich"}
{"entry_id": "CXdD-G1NXEJP9vy9fSU32w", "businessname": "Black Tap Craft Burgers And Beer", "address": "Werdmühlestrasse 4, 8001 Zürich"}
{"entry_id": "ubAA9IL3FCfUdAhAUAogsQ", "businessname": "La Bottega di Mario", "address": "Nüschelerstrasse 6, 8001 Zürich"}
{"entry_id": "X2CHbjTzwcLws7m4EUKoQQ", "businessname": "Michelangelo", "address": "Gertrudstrasse 37, 8003 Zürich"}
{"entry_id": "kdgDBy0uJFKOQNm7Fqa_bA", "businessname": "Osso", "address": "Zollstrasse 121, 8005 Zürich"}
{"entry_id": "Dzt8_2Mmh_EMz_Rc8Sia1A", "businessname": "ooo Rooftop Restaurant", "address": "Bahnhofstrasse 74, 8001 Zürich"}
{"entry_id": "O4VqYsdSUSChocHn0H8LSA", "businessname": "Die Waid", "address": "Waidbadstrasse 45, 8037 Zürich"}
{"entry_id": "wSj_UXGtjHLAnL4feZPvUA", "businessname": "Starbucks", "address": "Museumstrasse 1, 8001 Zürich"}
{"entry_id": "YzHhCosKtfGxh65TF0SzTA", "businessname": "Gelatissimo", "address": "Gessnerallee 8, 8001 Zürich"}
{"entry_id": "CveqVhKXpGSvBxa1PYHLMA", "businessname": "Hot Pasta AG", "address": "Universitätstrasse 15, 8006 Zürich"}
{"entry_id": "_dYXEVIJFpG9LpJDqJCGLA", "businessname": "Arctic Juice & Cafe", "address": "Sihlstrasse 20, 8001 Zürich"}
{"entry_id": "5p7CuLdBmtiXpZse2kYAlQ", "businessname": "Zum Frischen Max", "address": "Max-Frisch-Platz 25a, 8050 Zürich"}
{"entry_id": "AVbXT_bKjdCd8sjZYZMSPQ", "businessname": "cc.café", "address": "Hohlstrasse 484, 8048 Zürich"}
{"entry_id": "CvBHaAFSJ5uivDXOdi6rtQ", "businessname": "Wirtschaft zum Transit", "address": "Aargauerstrasse 14, 8048 Zürich"}
{"entry_id": "CNwWZ7kxZq8_ixz6omRjsQ", "businessname": "Pizzeria Libero", "address": "Badenerstrasse 451, 8003 Zürich"}
{"entry_id": "9nfYE0OMQlh5EzxHhvho0w", "businessname": "Santa Lucia Paradeplatz", "address": "Waaggasse 5-7, 8001 Zürich"}
{"entry_id": "v9uQDSkqzrpmytTb19aBJw", "businessname": "Manuel's", "address": "Löwenstrasse 12, 8001 Zürich"}
{"entry_id": "sTIglrfiv3rIiX_0TiiYWw", "businessname": "Restaurant 8048", "address": "Lindenplatz 5, 8048 Zürich"}
{"entry_id": "FaLRvl8vJEq9028umUMsQw", "businessname": "Restaurant Time Out", "address": "Hirschengraben 64, 8001 Zürich"}
{"entry_id": "xRV-YXmIRa13Nwd87zVPTg", "businessname": "James Joyce", "address": "Pelikanstrasse 8, 8001 Zürich"}
{"entry_id": "goUBgR08jM_gXZLyqrZnfg", "businessname": "Indisches Restaurant Kormasutra", "address": "Altstetterstrasse 130, 8048 Zürich"}
{"entry_id": "_7bXbVBKsmKOszhS7QPZfQ", "businessname": "Restaurant Heugümper", "address": "Waaggasse 4, 8001 Zürich"}
{"entry_id": "zfXw0TNSbqx9IptcpS9q8A", "businessname": "Bierhalle Kropf", "address": "In Gassen 16, 8001 Zürich"}
{"entry_id": "gxxbFik5Qo-PUJKdrQ9yCQ", "businessname": "Justus", "address": "Asylstrasse 70, 8032 Zürich"}
{"entry_id": "ib6RKssr9YBBb_K5vcJ8kw", "businessname": "QQ Sushi Zürich", "address": "Stampfenbachstrasse 6, 8001 Zürich"}
{"entry_id": "_goZB0nLkK0act-IB5Qz5Q", "businessname": "Collana Bar e Caffè", "address": "Theaterstrasse 9, 8001 Zürich"}
{"entry_id": "HmAbMppuEFoAso9Oy2HkMA", "businessname": "Piazzetta", "address": "Bahnhofstrasse 87, 8001 Zürich"}
{"entry_id": "Jy-ULP8UsyODWXEGCC8CxQ", "businessname": "Restaurant Elefant", "address": "Witikonerstrasse 279, 8053 Zürich"}
{"entry_id": "q3t5nGUXRb3ZNJq49fLusA", "businessname": "Not guilty Gastronomie AG", "address": "Emil-Oprecht-Strasse 1, 8050 Zürich"}
{"entry_id": "ZDoxMpUHWJgDpI-NhcA5pQ", "businessname": "Ali Osman Engin", "address": "Wallisellenstrasse 5, 80 50 Zürich"}
{"entry_id": "zNylkLrISlGc1qbqeP742w", "businessname": "Palette Restaurant Café Bar", "address": "Schützengasse 7, 8001 Zürich"}
{"entry_id": "NPcu-YOtUZUucLtf_TuCJA", "businessname": "Indojaya GmbH", "address": "Schaffhauserstrasse 373, 8050 Zürich"}
{"entry_id": "WrpF74bGPnuuJM8t5ghytg", "businessname": "Restaurant Ö", "address": "Schaffhauserstrasse 335, 8050 Zürich"}
{"entry_id": "IM4nufmoQ1LGNCgYgpCs8w", "businessname": "Metzgerhalle", "address": "Schaffhauserstrasse 354, 8050 Zürich"}
{"entry_id": "qCI6i8wWIPBPXro_2Ugjag", "businessname": "Restaurant Riedbach", "address": "Hagenholzstrasse 104A, 8050 Zürich"}
{"entry_id": "KliQpHZXv6GKc9dzMjoWww", "businessname": "China-Restaurant King To", "address": "Badenerstrasse 816, 8048 Zürich"}
{"entry_id": "iJSv9hNWUtnKWi4vuKxxVQ", "businessname": "Nooch Asian Kitchen Zürich Badenerstrasse", "address": "Badenerstrasse 101, 8004 Zürich"}
{"entry_id": "HguAJpNl911s21ieYcWC3w", "businessname": "Restaurant Viadukt", "address": "Viaduktstrasse 69, 8005 Zürich"}
{"entry_id": "q9H8zaq1sx4Mew_KLmXlVQ", "businessname": "Michelle's Cupcakes", "address": "Luisenstrasse 19, 8005 Zürich"}
{"entry_id": "3x-F1j_SKhQ2PVCnF9yz0g", "businessname": "Tritt Käse im Viadukt AG", "address": "Limmatstrasse 231, 8005 Zürich"}
{"entry_id": "y3p6HMFOtNOUYUwgMTbQVA", "businessname": "Restaurant Fischerstube", "address": "Bellerivestrasse 160, 8008 Zürich"}
{"entry_id": "QnwubNPSPyuLP_1jcOtOHQ", "businessname": "O'k Gemüsedöner", "address": "Freilagerstrasse 11, 8047 Zürich"}
{"entry_id": "yP-bg9Athx197F_gTlGa0g", "businessname": "Sternen", "address": "Albisriederstrasse 371, 8047 Zürich"}
{"entry_id": "ZBEldLCcod25V-KY3KLs7g", "businessname": "Bistro Albisrieden", "address": "Albisriederstrasse 358, 8047 Zürich"}
{"entry_id": "yAD2v7nsKY_yCPaEMHj9wg", "businessname": "Grainglow Gmbh", "address": "Albisriederstrasse 253, 8047 Zürich"}
{"entry_id": "uYq0jLI3OwJFFN8P2jxX-g", "businessname": "Spaghetti Factory Rosenhof", "address": "Niederdorfstrasse 5, 8001 Zürich"}
{"entry_id": "qnilEbBpz5djc3P2ngHs3g", "businessname": "Test_Nast", "address": "H 120, 8005 Zürich"}
{"entry_id": "pUTWWiCNQ1hmBIsnvzQMRA", "businessname": "Zimmi's Bistro", "address": "Schaffhauserstrasse 433, 8050 Zürich"}
{"entry_id": "ygsSP5TRDS5gtxhSi0Cj3g", "businessname": "Bongusto Cookies & Ice Cream", "address": "Niederdorfstrasse 37, 8001 Zürich"}
{"entry_id": "wFA4lXLT-N8s-ydfRlNFoQ", "businessname": "Brooklyn Burger", "address": "Kasernenstrasse 77B, 8004 Zürich"}
{"entry_id": "h7rLuZCoSJoNRneiTLm1Aw", "businessname": "Bäckerei Konditorei Tanner", "address": "Schaffhauserstrasse 427, 8050 Zürich"}
{"entry_id": "lukKwp0EoQhkZ6IzGd5yXA", "businessname": "Enzian Cafébar", "address": "Thurgauerstrasse 36, 8050 Zürich"}
{"entry_id": "6sfIkSZBtHXCH3tKU1X6KA", "businessname": "McDonald's", "address": "Niederdorfstrasse 30, 8001 Zürich"}
{"entry_id": "Jh7-KB9kNclA-a39dBTy8A", "businessname": "Williams ButchersTable Bellevue", "address": "Schifflände 6, 8001 Zürich"}
{"entry_id": "njmQVlbFG8GV407YfD23SA", "businessname": "Yi Long Asia Restaurant", "address": "Magnusstrasse 16, 8004 Zürich"}
{"entry_id": "QJ_R6pZx1s91PhXS2xnhag", "businessname": "Mensa FKSZ", "address": "Kreuzbühlstrasse 16, 8008 Zürich"}
{"entry_id": "n-BWhLnW_CQoV6fyxsJARg", "businessname": "dieci Pizza Kurier Zürich Binz-Wollishofen", "address": "Eibenstrasse 24, 8045 Zürich"}
{"entry_id": "vKHyOsZVcOzqXylQ7PFF7A", "businessname": "Thai Bamboo", "address": "Schoffelgasse 3, 8001 Zürich"}
{"entry_id": "osIeBEOiSevcEDyeAlLIFQ", "businessname": "Burgermeister Langstrasse", "address": "Langstrasse 6, 8004 Zürich"}
{"entry_id": "NYlhWa4I2DK8AT6bEtMV4g", "businessname": "Läckerli Huus AG", "address": "8001 Zürich"}
{"entry_id": "te9dFV16QamBhIXPXnWfpw", "businessname": "YUMA Restaurant & Bar", "address": "Badenerstrasse 120, 8004 Zürich"}
{"entry_id": "jsFh4ufxNiSMGa4mX8oPmw", "businessname": "Walliser Keller SwissAlpeChuchi", "address": "Zähringerstrasse 21, 8001 Zürich"}
{"entry_id": "XD2xhjEQmCba3XR30tmipQ", "businessname": "Ba Ba Lu Bar", "address": "Schmidgasse 6, 8001 Zürich"}
{"entry_id": "JsOw-LT4kP0k8plOeca1pw", "businessname": "Ebrietas Bar", "address": "Zähringerstrasse 39, 8001 Zürich"}
{"entry_id": "x_7yL2O-RL7GcKnzI-V4sw", "businessname": "At Chuck's", "address": "8048 Zürich"}
{"entry_id": "DwyKKdsjbKPnbKrQjA1P1g", "businessname": "my Mythos GmbH", "address": "Stauffacherstrasse 35, 8004 Zürich"}
{"entry_id": "ly_q0RuZR_iPtOdrfzrV9w", "businessname": "HITZBERGER Sihlcity", "address": "Kalanderplatz 1, 8045 Zürich"}
{"entry_id": "quUEW99eCCv5ygpLN6CsRQ", "businessname": "Bar Rossi", "address": "Sihlhallenstrasse 3, 8004 Zürich"}
{"entry_id": "zqBCu2WR7sJXy0QWbC3s9w", "businessname": "Franzos", "address": "Limmatquai 138, 8001 Zürich"}
{"entry_id": "lL_2RmLqlpfBDhlWd9M5wA", "businessname": "Pao Pao - Modern Tea - Zurich", "address": "Badenerstrasse 156, 8004 Zürich"}
{"entry_id": "0ah5c5W6mhJoUfKy4dH04A", "businessname": "Asia Sytyle Cooking", "address": "Langstrasse 117, 8004 Zürich"}
{"entry_id": "nVESaL0TOav64BpX8B1Ncg", "businessname": "CUPCAKE AFFAIR GmbH", "address": "Spitalgasse 10, 8001 Zürich"}
{"entry_id": "y7G0HQ3fJp4yzQxx2xQFJA", "businessname": "Robin's little Italy", "address": "Zähringerstrasse 33, 8001 Zürich"}
{"entry_id": "vpxonT5CI2Z6Y72pkHEwdw", "businessname": "Store Kreuzplatz", "address": "Kreuzplatz 22, 8008 Zürich"}
{"entry_id": "JSJ8Yb1R5RDzEzvMm03GPg", "businessname": "Sc hwarzes Schaf - Bistrolino & Bar", "address": "Langstrasse 10, 8004 Zürich"}
{"entry_id": "Vwa7lj1C5rqDqBC-0fvkXA", "businessname": "Lele", "address": "Militärstrasse 76, 8004 Zürich"}
{"entry_id": "nKWotM1QFLuabeJKWpl1Jg", "businessname": "Restaurant Schwamedinge", "address": "Schwamendingerplatz 2, 8051 Zürich"}
{"entry_id": "YenYf0HF1NebzWXSu1TFAA", "businessname": "Jane Fine Food", "address": "Erlachstrasse 46, 8003 Zürich"}
{"entry_id": "xOsLr9V4nJXwYZCvLxZHdw", "businessname": "Restaurant Ach'i", "address": "Brauerstrasse 4, 8004 Zürich"}
{"entry_id": "ptGCSifyDLkpIn1C426FQQ", "businessname": "Fondue Stübli", "address": "Rotwandstrasse 38, 8004 Zürich"}
{"entry_id": "gVi9nsRXjubk0M8YvadEuw", "businessname": "Wolf Bierhalle", "address": "Limmatquai 132, 8001 Zürich"}
{"entry_id": "rKBL-eeub7s-hQbo1uPn1g", "businessname": "Ristorante Frascati", "address": "Bellerivestrasse 2, 8008 Zürich"}
{"entry_id": "GTZqSP47NlEajt0NtuLmtQ", "businessname": "Pizzeria Ristorante Molino Select", "address": "Limmatquai 16, 8001 Zürich"}
{"entry_id": "5ZtWvQUJfeYRyJIxI2e0Hg", "businessname": "Restaurant zum Grünen Glas", "address": "Untere Zäune 15, 8001 Zürich"}
{"entry_id": "qsF3Cyix_a_EOylY1j9icQ", "businessname": "Bürgli", "address": "Kilchbergstrasse 15, 8038 Zürich"}
{"entry_id": "cAJ9muHxJGSr4f6aW-Truw", "businessname": "Bederhof", "address": "Brandschenkestrasse 177, 8002 Zürich"}
{"entry_id": "o1IwZprMCdQQpokP647lhA", "businessname": "Schönau Bar Restaurant", "address": "Hohlstrasse 78, 8004 Zürich"}
{"entry_id": "mjskVeQsruz29R02aVBaGg", "businessname": "GAINSBOURG", "address": "Kreuzstrasse 26, 8008 Zürich"}
{"entry_id": "9Fyly1sg3P6HpFLlGzcRvw", "businessname": "Lake Side", "address": "Bellerivestrasse 170, 8008 Zürich"}
{"entry_id": "ku9KKCl3NEfLVpf306MjXA", "businessname": "Bar Corazon", "address": "Zähringerplatz 11, 8001 Zürich"}
{"entry_id": "K6WSfUizFBN2FrHIQQgrbQ", "businessname": "Yokita - japanisches Take Away", "address": "Friesenbergstrasse 3, 8055 Zürich"}
{"entry_id": "z2qh3FrdtSZI5VnjlmBKRQ", "businessname": "The Traders", "address": "Leutschenbachstrasse 95, 8050 Zürich"}
{"entry_id": "uhUFK0loY8ASCg7Ww3yFkg", "businessname": "Treff Restaurant-Bar", "address": "8046 Zürich"}
{"entry_id": "1nZN_KapCRmVs9ZnFWeFbw", "businessname": "Bridge", "address": "Europaallee 22, 8004 Zürich"}
{"entry_id": "vR4bMDntsWEMepv6hKphCA", "businessname": "Starbucks", "address": "Limmatquai 4, 8001 Zürich"}
{"entry_id": "U6ip9Je5RmaR5_Zl0-Mwfw", "businessname": "Gran Café Motta", "address": "Limmatquai 66, 8001 Zürich"}
{"entry_id": "Iawvt6K4UYoWzw1DQnWW1Q", "businessname": "Regenbogen Bar", "address": "Rosengasse 6, 8001 Zürich"}
{"entry_id": "2WBGVDPb-t0L3DXEbmEUmg", "businessname": "Königstuhl Gastronomie AG", "address": "Stüssihofstatt 3, 8001 Zürich"}
{"entry_id": "E4PRpGB_XvKldBB997onCA", "businessname": "Zeder", "address": "Badenerstrasse 78, 8004 Zürich"}
{"entry_id": "Odpfu2gF063riEgLb0RUzg", "businessname": "Robin's Coffee", "address": "Zähringerstrasse 33, 8001 Zürich"}
{"entry_id": "PYqicaf3HuGpW86SXvPnIg", "businessname": "Blue Monkey - Authentic Thai Restaurant", "address": "Stüssihofstatt 3, 8001 Zürich"}
{"entry_id": "rOk4JftiGIaruIOBrEl0gg", "businessname": "Vesuvio Pizzeria Da Antonio", "address": "Glatttalstrasse 40, 8052 Zürich"}
{"entry_id": "LMS3oC1ON2AhRdbFXmKflQ", "businessname": "China Restaurant Chop-Stick", "address": "Niederdorfstrasse 82, 8001 Zürich"}
{"entry_id": "bf6de36tXC_KcjYCN17b1A", "businessname": "Schnupf", "address": "Neufrankengasse 29, 8004 Zürich"}
{"entry_id": "auswhz3dG0isYjZXyuFwLg", "businessname": "Ristorante La Pasta AG", "address": "Niederdorfstrasse 80, 8001 Zürich"}
{"entry_id": "p070TsdEjhstjgkDZb3R3w", "businessname": "Winter Garte Europaallee Zürich", "address": "Gustav-Gull-Platz, 8004 Zürich"}
{"entry_id": "SDTb-wE1gBaeBXuSCv3qZw", "businessname": "Ristorante Pizzeria Don Emilio", "address": "Dübendorfstrasse 24, 8051 Zürich"}
{"entry_id": "RZEpT4XvanBRSghcba7B_g", "businessname": "FELFEL AG", "address": "Grubenstrasse 11, 8045 Zürich"}
{"entry_id": "sl3WAKssnNCNWVNclYLybA", "businessname": "Kantorei", "address": "Spiegelgasse 33, 8001 Zürich"}
{"entry_id": "Xkqvx2F1J3k4Mkd60p-RyA", "businessname": "Restaurant Ländli Züri", "address": "Feldeggstrasse 87, 8008 Zürich"}
{"entry_id": "NIQfc90KxOjHIrNDGS5wAQ", "businessname": "John Baker Helvetia Ltd.", "address": "Molkenstrasse 15, 8004 Zürich"}
{"entry_id": "FZ8apve1S3xjkVynGTRAqA", "businessname": "Imbiss Riviera", "address": "Utoquai 2, 8008 Zürich"}
{"entry_id": "hGpFjfj4qdifNKWeTT5ZDg", "businessname": "Vasco's Bar", "address": "Bäckerstrasse 20, 8004 Zürich"}
{"entry_id": "iYYBBw4rzOyifDU1EdBsHQ", "businessname": "Hotel Hirschen", "address": "Niederdorfstrasse 13, 8001 Zürich"}
{"entry_id": "8MZgnVV2l6sORbzD8bMgyQ", "businessname": "Ristorante Più Europaallee", "address": "Kasernenstrasse 95, 8004 Zürich"}
{"entry_id": "FRM8rwp_-V8gO6Ko6GChRw", "businessname": "Restaurant Volkshaus", "address": "Stauffacherstrasse 60, 8004 Zürich"}
{"entry_id": "6b6_4CXIyn9J94yKDxCDeQ", "businessname": "Filini Restaurant", "address": "Postfach 295, 8058 Zürich"}
{"entry_id": "--4_mVtsTB60xycsWAE6EA", "businessname": "Cristina Test", "address": "Berninaplatz 2, 8057 Zürich"}
{"entry_id": "T3x8IL6LrMteVrw2sK8jlA", "businessname": "Thai Bogie Kitchen", "address": "Neunbrunnenstrasse 50, 8050 Zürich"}
{"entry_id": "87kgOtDY0eEUa6-JEGmb7w", "businessname": "Smeily's", "address": "Bernistrasse 43  Oerlikon, 8057 Zürich"}
{"entry_id": "oFCqW_DvzGXc0sRxfdXi9g", "businessname": "Träffpunkt", "address": "Regensbergstrasse 188, 8050 Zürich"}
{"entry_id": "HZf9fYnhQMCAZMCj1Yib-A", "businessname": "Restaurant Neue Taverne", "address": "Glockengasse 8, 8001 Zürich"}
{"entry_id": "tu7sKw7PQYEEvawwWlBOZA", "businessname": "Panama Bar - Grill", "address": "Lettensteg 10, 8037 Zürich"}
{"entry_id": "EoCNsf-7k8Mv1siijeSrBQ", "businessname": "Nüni", "address": "Hohlstrasse 430, 8048 Zürich"}
{"entry_id": "IEpVYSQs2fJHefRLIGgUqw", "businessname": "Café & Beck Oberstrass", "address": "Universitätstrasse 9, 8006 Zürich"}
{"entry_id": "JZ9BgkElQFwF3V8os1aXug", "businessname": "Maki Haus Inh. Yao", "address": "Stampfenbachstrasse 12, 8001 Zürich"}
{"entry_id": "DolGkCh_RxQ9nAsBq90i9w", "businessname": "Steakhaus & Pizzeria Mattenhof", "address": "Dübendorfstrasse 321, 8051 Zürich"}
{"entry_id": "Wzmdaon4fatknoNRbxW_Gw", "businessname": "Alters - und Pflegezentrum Herrenbergli, Zürich-Altstetten", "address": "Am Suteracher 65, 8048 Zürich"}
{"entry_id": "mYoSNlOLmcgOfqd1_0nihw", "businessname": "Lenox Bar", "address": "Neumühlequai 42, 8006 Zürich"}
{"entry_id": "nXK1lySWOQE8-uT9HbHdoQ", "businessname": "Anoah - Plant Based", "address": "Rigiplatz 1, 8006 Zürich"}
{"entry_id": "ZbsOxmjAvUqvzXR5YXi2bw", "businessname": "S. Ip's Pub", "address": "Schaffhauserstrasse 380, 8050 Zürich"}
{"entry_id": "wxLajjkJUmDuSHiZPBQ5nA", "businessname": "Restaurant Bernadette", "address": "Sechseläutenplatz 1, 8001 Zürich"}
{"entry_id": "7OqrJZsSMgO4GInyDOd_SQ", "businessname": "Restaurant Spitz", "address": "Museumstrasse 2, 8001 Zürich"}
{"entry_id": "F_oqZH7lhMCRwXjiHweuVg", "businessname": "Dr. Zhivago AG", "address": "Bärengasse 29, 8001 Zürich"}
{"entry_id": "QFF-4OC5HNrhsBLMMglHyQ", "businessname": "Züri Burg", "address": "Badenerstrasse 659, 8048 Zürich"}
{"entry_id": "Ah-38M1XR1AJK0dlizBJjw", "businessname": "Restaurant Münsterhof", "address": "Münsterhof 6, 8001 Zürich"}
{"entry_id": "j8B4XwZOUom2bQtzx14NgQ", "businessname": "Josef", "address": "Gasometerstrasse 24, 8005 Zürich"}
{"entry_id": "sSeFvTUgntRAd0r7xoDidw", "businessname": "Yooji's Passage Sihlquai", "address": "Museumstrasse 1, 8001 Zürich"}
{"entry_id": "GWKVgM6vlrhQgXEEzLJpnw", "businessname": "Haute SA", "address": "Talstrasse 65, 8001 Zürich"}
{"entry_id": "wt-SrDdz5QsPWAjVhePLUA", "businessname": "SAM'S Pizza Land", "address": "Schweizergasse 6, 8001 Zürich"}
{"entry_id": "4JM7Qimpdip5SgwMHEXgTA", "businessname": "Chaima Thai Take Away GmbH", "address": "Lägernstrasse 32, 8037 Zürich"}
{"entry_id": "YQGL32WHaEnI6Q-xIru08A", "businessname": "Imagine", "address": "8001 Zürich"}
{"entry_id": "esPyDxYOEJYF6AEohcB5HA", "businessname": "Lumière AG", "address": "Widdergasse 5, 8001 Zürich"}
{"entry_id": "sfr1guUd5BFWUEPvRs03Gg", "businessname": "Musti Grill", "address": "Saumackerstrasse 48, 8048 Zürich"}
{"entry_id": "rBItADCQPzNsvCVrwYdWtw", "businessname": "Restaurant Burgwies", "address": "Forchstrasse 271, 8008 Zürich"}
{"entry_id": "NU-rSFZW6o1iJ20pABoSHA", "businessname": "Cheyenne", "address": "Querstrasse 3, 8050 Zürich"}
{"entry_id": "W91yhXn3A7SsRr4_1MTqaA", "businessname": "Ellermann 's Hummerbar", "address": "Bahnhofstrasse 87, 8001 Zürich"}
{"entry_id": "E2FE14_t_A8FFW9_xUkXBQ", "businessname": "George Bar & Grill", "address": "Gessnerallee 5, 8001 Zürich"}
{"entry_id": "4judvzzAu37tGMZ2JoEz8Q", "businessname": "Curry Queen", "address": "Badenerstrasse 663, 8048 Zürich"}
{"entry_id": "rq5Bkt5YgsPIaoycH0YwlA", "businessname": "Churrasco Steak & Nikkei Cuisine", "address": "Glockengasse 9, 8001 Zürich"}
{"entry_id": "3puXcuzInvHY75hC5YU6AQ", "businessname": "Il Pentagramma", "address": "Josefstrasse 28, 8005 Zürich"}
{"entry_id": "f8mBzVzuliu3x8uMUOR11Q", "businessname": "Sprössling", "address": "Hotzestrasse 65, 8006 Zürich"}
{"entry_id": "Xj44swhjOqEaXWEnW9CT7A", "businessname": "Parea", "address": "Zentralstrasse 161, 8003 Zürich"}
{"entry_id": "kgcY-7Brw-cIuOBIJjGv9Q", "businessname": "VAPIANO", "address": "Rämistrasse 8, 8001 Zürich"}
{"entry_id": "HwTkY_u1CXxCT7gdnMCOAg", "businessname": "Lotti Restaurant Bar Cafe Grill", "address": "Werdmühleplatz 3, 8001 Zürich"}
{"entry_id": "bOnLwqK2IMVUHPihMwa8bQ", "businessname": "Casino Restaurant", "address": "Badenerstrasse 647, 8048 Zürich"}
{"entry_id": "pGBZL2dxHT1UDfWHKFWKBA", "businessname": "Restaurant Thai Erawan", "address": "Badenerstrasse 811, 8048 Zürich"}
{"entry_id": "jhOjJPylVqidkQRcSuEAtA", "businessname": "Zunfthaus zum Widder", "address": "Rennweg 7, 8001 Zürich"}
{"entry_id": "-JvxPXQf4cuchLqjsZzX5A", "businessname": "McDonald's", "address": "Gottfried-Keller-Strasse 7, 8001 Zürich"}
{"entry_id": "zVDz9IOruY5UszDAf36TwQ", "businessname": "Restaurant Oval", "address": "Badenerstrasse 500, 8048 Zürich"}
{"entry_id": "Yb_rYkJF2m1xVbpJeHz-fA", "businessname": "Restaurant Hato", "address": "Brandschenkestrasse 20, 8001 Zürich"}
{"entry_id": "ZuM_2ihNQSp5gVoqFeay2Q", "businessname": "Namamen", "address": "Vulkanplatz 9, 8048 Zürich"}
{"entry_id": "oMVxcBGUH4IgpHzBhgL4rg", "businessname": "Zurich Fine Chocolate and Cake", "address": "Waserstrasse 76, 8053 Zürich"}
{"entry_id": "50Q67kcmvE_FPE-zx9zkvg", "businessname": "MyLOCALINA Free Showcase (FR)", "address": "Förrlibuckstrasse 62, 8005 Zürich"}
{"entry_id": "xi32XFsUAWwpbUKCsnxkcA", "businessname": "Restaurant Vulkan", "address": "Klingenstrasse 33, 8005 Zürich"}
{"entry_id": "js1V8FX4imLlcxRUoNAkXg", "businessname": "YUKA - Restau rant & Bar", "address": "Stampfenbachstrasse 60, 8006 Zürich"}
{"entry_id": "4Y7v1IpAubUxGlr3yTHikg", "businessname": "Il Punto", "address": "Zschokkestrasse 1, 8037 Zürich"}
{"entry_id": "XlOM3DSqSoeHWjGtRZozEw", "businessname": "Haus Hiltl", "address": "Sihlstrasse 28, 8001 Zürich"}
{"entry_id": "8XAemi_ipOq-UdiIfJI8Pw", "businessname": "Restaurant R21", "address": "Orellistrasse 21, 8044 Zürich"}
{"entry_id": "eDDH6OTlSl9qcj3_7kNWPQ", "businessname": "SBB Restaurant Oase", "address": "8001 Zürich"}
{"entry_id": "1um85w1y9hhMWOSujXYfcw", "businessname": "Restaurant Pavillon", "address": "Talstrasse 1, 8001 Zürich"}
{"entry_id": "76FPInMVFXpDvaGYztXSBA", "businessname": "Lobby", "address": "Bahnhofstrasse 87, 8001 Zürich"}
{"entry_id": "4gxowGVKbgS7l26PTmAgtQ", "businessname": "Jules Verne Panoramabar", "address": "Uraniastrasse 9, 8001 Zürich"}
{"entry_id": "CG8bQYi4A9UG4GPtacqqgA", "businessname": "Schmiedhof Alters- und Pflegeheim", "address": "Zweierstrasse 138, 8003 Zürich"}
{"entry_id": "53M1g1dEJqqVQ2TAqBCDkg", "businessname": "Friends Corner", "address": "Josefstrasse 146, 8005 Zürich"}
{"entry_id": "P3husr1GCG6i7yvdUNGn4w", "businessname": "Aroma", "address": "Asylstrasse 110, 8032 Zürich"}
{"entry_id": "0TsjbrVp93g0B2_2yXFrUw", "businessname": "4. Akt", "address": "Heinrichstrasse 262, 8005 Zürich"}
{"entry_id": "pv-x3LBNbYUmWtBr7gbirw", "businessname": "Tapas & Friends", "address": "Aemtlerstrasse 86, 8003 Zürich"}
{"entry_id": "W-Zay401NcMFZeIDx4kavA", "businessname": "Store Stadelhofen", "address": "Theaterstrasse 8, 8001 Zürich"}
{"entry_id": "Fg3lUB0JB1cS4SkENIKHVg", "businessname": "Jamaican Flavour", "address": "Langstrasse 200, 8005 Zürich"}
{"entry_id": "xPNMLk1ZleTNjeIW8ierjw", "businessname": "Gelateria Di Berna", "address": "Weststrasse 196, 8003 Zürich"}
{"entry_id": "Nmy6we8IHBZrleNrzhuDAQ", "businessname": "Zoocafé", "address": "Zürichbergstrasse 219, 8044 Zürich"}
{"entry_id": "Vp--1CamLPnXEI4Qi-cfrA", "businessname": "Zur Taverne WeinArt", "address": "Imbisbühlstrasse 7, 8049 Zürich"}
{"entry_id": "cAkBYHpHyEhXDTtRO_i_Ow", "businessname": "dean & david ZH Bleicherweg GmbH", "address": "Bleicherweg 19, 8002 Zürich"}
{"entry_id": "KSXyJ3WLBMhr3vHCQbuCiA", "businessname": "Yooji's Josef", "address": "Josefstrasse 112, 8005 Zürich"}
{"entry_id": "IyYTEwOjHz_tdKABndLpkQ", "businessname": "Panorama Restaurant Albisgütli", "address": "Uetlibergstrasse 331, 8045 Zürich"}
{"entry_id": "SPdRx8sTHn0y4od94X-aDA", "businessname": "Bibim Shack", "address": "Hardstrasse 322, 8005 Zürich"}
{"entry_id": "VcoAdIEPQr0DAFaE3B0p6A", "businessname": "Margheri", "address": "Limmatstrasse 273, 8005 Zürich"}
{"entry_id": "_2GdVCRXmtinI_PDX04Ouw", "businessname": "il bistrò", "address": "Konradstrasse 40, 8005 Zürich"}
{"entry_id": "2NVZ8SS13bUH_eD-c9-60w", "businessname": "Napi's Thai Restaurant & Take Away", "address": "Flurstrasse 4, 8048 Zürich"}
{"entry_id": "MycWn5pw2nF5md4WXsNHLg", "businessname": "Pizzeria Unico", "address": "Limmatstrasse 273, 8005 Zürich"}
{"entry_id": "YSBt7D1CzyB4pQvcTt9RWw", "businessname": "Sai Somsak", "address": "Neue Hard 9, 8005 Zürich"}
{"entry_id": "P_QiM7s_0K2UYUMFxTZ61A", "businessname": "Pause im Foifi", "address": "Förrlibuckstrasse 70, 8005 Zürich"}
{"entry_id": "z2TJMdR3P13K74Wqq3mDwg", "businessname": "Martin Puppel Architekt", "address": "Dorfstrasse 40, 8037 Zürich"}
{"entry_id": "LmSQOuVdrCwiiJbikdDDtA", "businessname": "Bäckerei Hug", "address": "Goethestrasse 14, 8001 Zürich"}
{"entry_id": "M6l7Qg2LxgEKshf-cMiuxQ", "businessname": "Lily's", "address": "Langstrasse 197, 8005 Zürich"}
{"entry_id": "ebL5lpmoGyOe66NPGjymgA", "businessname": "Al Mouchtar", "address": "Hafnerstrasse 13, 8005 Zürich"}
{"entry_id": "zfLN80ZlqkE3bL3XhDuInQ", "businessname": "Iberico", "address": "Milchbuckstrasse 11, 8057 Zürich"}
{"entry_id": "1_J7HVsc8xdR0bjh--EBcw", "businessname": "Alegria Restaurante Peruano", "address": "Seestrasse 361, 8038 Zürich"}
{"entry_id": "7MxE3WGKmZo8yWmqlGLtmw", "businessname": "25hours Hotel Zürich West", "address": "Pfingstweidstrasse 102, 8005 Zürich"}
{"entry_id": "u7n_c4xXz_8PHU25Jghn-Q", "businessname": "Starbucks Coffee", "address": "Winterthurerstrasse 698, 8051 Zürich"}
{"entry_id": "W7z76pmwquA3CALe67NzAg", "businessname": "Route twenty-six", "address": "Pfingstweidstrasse 100, 8005 Zürich"}
{"entry_id": "OlEmxhIfqiwo1q4S5XYr_g", "businessname": "Restaurant Haldenbach", "address": "Haldenbachstrasse 2, 8006 Zürich"}
{"entry_id": "TcUB_uVt5dZdkdr7m6YlCA", "businessname": "Soul St Zurich", "address": "Döltschiweg 234, 8055 Zürich"}
{"entry_id": "V6PwrJ20W-0PGPxBF2o47A", "businessname": "apoTHEKE Gastro AG", "address": "Zürichbergstrasse 17, 8032 Zürich"}
{"entry_id": "extXgA1oQCOX8TVdxpJZSw", "businessname": "Nishi Japan Shop", "address": "Schaffhauserstrasse 120, 8057 Zürich"}
{"entry_id": "umvLfWqH7j3lVg8jrXrN2Q", "businessname": "Dune Oriental Lounge Privatclub", "address": "Josefstrasse 29, 8005 Zürich"}
{"entry_id": "qnpeRTKRnm2rUQRRHLvx0w", "businessname": "Restaurant Weisses Rössli", "address": "Bederstrasse 96, 8002 Zürich"}
{"entry_id": "RBUKNfajQC1y4ies4a2RVg", "businessname": "Domino's Pizza Zürich Goldbrunnen", "address": "Goldbrunnenstrasse 115, 8055 Zürich"}
{"entry_id": "qPQ2u2uUQBxJ8thcccwKDg", "businessname": "Tremonte Catering GmbH", "address": "Birmensdorferstrasse 129, 8003 Zürich"}
{"entry_id": "_Jeyw_HbIZVo4H-6Qty-3w", "businessname": "Costa Brava", "address": "Limmatstrasse 267, 8005 Zürich"}
{"entry_id": "cwoYfOSqISahxaz64nCp6w", "businessname": "Rosaly's Restaurant & Bar", "address": "Freieckgasse 7, 8001 Zürich"}
{"entry_id": "gCN7t1vHL33sJTelEPrpsg", "businessname": "Tillsamman GmbH", "address": "Sihlfeldstrasse 10, 8003 Zürich"}
{"entry_id": "qRfr42BwOKKzeuN9o8fZyQ", "businessname": "ease DESIGN SPA", "address": "Giessereistrasse 18, 8005 Zürich"}
{"entry_id": "bAbSw1KgA_y7ZMcdlHFbSA", "businessname": "Chop Chop Asian Delight", "address": "Josefstrasse 102, 8005 Zürich"}
{"entry_id": "2eFu_KcEvsKwg1R6aYMcOw", "businessname": "Züri Bistro Milchbuck", "address": "Schaffhauserstrasse 126, 8057 Zürich"}
{"entry_id": "AQBT2dbVgNKBbvY8KI93_g", "businessname": "Sushi Palace", "address": "Thurgauerstrasse 23, 8050 Zürich"}
{"entry_id": "ZehDEfIpv_tdrXMZuTBWAA", "businessname": "Jaime El Barco", "address": "Otto-Schütz-Weg 5, 8050 Zürich"}
{"entry_id": "SoUa0szgz3SZL7jigq8ZZg", "businessname": "Restaurant Rosi", "address": "Sihlfeldstrasse 89, 8004 Zürich"}
{"entry_id": "0PuaRwY2oBBqcf4C0lsIDw", "businessname": "Bubbles", "address": "Werdstrasse 54, 8004 Zürich"}
{"entry_id": "Xrzcd_fzchn0y1nhORnXNQ", "businessname": "Astra Kitchen & Bar", "address": "Löwenstrasse 25, 8001 Zürich"}
{"entry_id": "cfuNusCpHwrDBjbw8Nmk6A", "businessname": "Restaurant Tschingg Oerlikon", "address": "Schaffhauserstrasse 353, 8050 Zürich"}
{"entry_id": "HEQfKX7yuZGEUMQHfQaUcQ", "businessname": "Confiserie Baumann AG", "address": "Balgriststrasse 2, 8008 Zürich"}
{"entry_id": "F5hI5F2ncnuWlrOb7cUEvw", "businessname": "Restaurant Lalina Ag", "address": "Thurgauerstrasse 23, 8050 Zürich"}
{"entry_id": "Oc7WK8XJQHBGsH4vq1JG1A", "businessname": "Burgstein's Gasthaus Penalty", "address": "Hallwylstrasse 40, 8004 Zürich"}
{"entry_id": "-ZSdi9Me9HG5w2Xe5FnA5g", "businessname": "Bros Beans & Beats", "address": "Gartenhofstrasse 24, 8004 Zürich"}
{"entry_id": "l1tWUuiVfxuTq0FmtASkdw", "businessname": "Fu Lin Asia Restaurant", "address": "Hohlstrasse 189, 8004 Zürich"}
{"entry_id": "UptxdqVG4rdLPNZAHhnY2w", "businessname": "Fulin", "address": "Hohlstrasse 189, 8004 Zürich"}
{"entry_id": "mTNO45RB1eoYO2woehsq1g", "businessname": "Vongole’s Kitchen", "address": "Forchstrasse 225, 8032 Zürich"}
{"entry_id": "TthHp0O8rk7huRWPqFdZ0w", "businessname": "Huusbeiz", "address": "Badenerstrasse 310, 8004 Zürich"}
{"entry_id": "XljInGjeCkOaoKqh3LIKkw", "businessname": "Popeyes Louisiana Kitchen", "address": "Baslerstrasse 50, 8048 Zürich"}
{"entry_id": "ra5VJyI3_VeREaqnSncz2w", "businessname": "Kochstudio Mangostan L. Richter", "address": "Albisriederstrasse 182a, 8047 Zürich"}
{"entry_id": "_f3C-Y0mtyT_W_JNibaayg", "businessname": "Restaurant Gandria", "address": "Rudolfstrasse 6, 8008 Zürich"}
{"entry_id": "gBnbFY8jTgq9otHf6FJM-A", "businessname": "Café Restaurant Mühlebach", "address": "Mühlebachstrasse 43, 8008 Zürich"}
{"entry_id": "0HVEL1zybwBsZZ8VgcDyJg", "businessname": "Test_Nast", "address": "H 120, 8005 Zürich"}
{"entry_id": "iswaq9ZflA7yIzwJl9nOyA", "businessname": "Wirtschaft Ziegelhütte", "address": "Hüttenkopfstrasse 70, 8051 Zürich"}
{"entry_id": "qM5aUF84g4qduM6l4h5ZrQ", "businessname": "Zum Roten Kamel", "address": "Niederdorfstrasse 1, 8001 Zürich"}
{"entry_id": "yHze1dYraNOaiKNW0vL2hg", "businessname": "Chickeria Langstrasse", "address": "Langstrasse 83, 8004 Zürich"}
{"entry_id": "KEH3iuvc3i4TdGGnbjEQSA", "businessname": "Gasthof Hirschen", "address": "Winterthurerstrasse 519, 8051 Zürich"}
{"entry_id": "ONFzzxtBCES3Gg-uNit5qQ", "businessname": "McDonald's Restaurant", "address": "Kalanderplatz 1, 8045 Zürich"}
{"entry_id": "hykxwoj8BRPfwtivczTxwA", "businessname": "Bauschänzli", "address": "Stadthausquai 2, 8001 Zürich"}
{"entry_id": "pAMZWEV56zOsxYF4mlYJjg", "businessname": "Hong Kong Vertex AG", "address": "Thurgauerstrasse 32, 8050 Zürich"}
{"entry_id": "y5ABRQ6qwPJLZC_lnnhpHg", "businessname": "Metzg", "address": "Seefeldstrasse 159, 8008 Zürich"}
{"entry_id": "weWnQ28e7x-Bp4cOl8cJyg", "businessname": "barfussbar", "address": "Stadthausquai 12, 8001 Zürich"}
{"entry_id": "p2ivIzD5-VdBZUT6S-QHZw", "businessname": "Yalla Habibi 2 Restaurant & Shisha Lounge", "address": "Birmensdorferstrasse 191, 8003 Zürich"}
{"entry_id": "BKdhExXVUTQokyu5XdDQsQ", "businessname": "Restaurant Blume", "address": "Winterthurerstrasse 534, 8051 Zürich"}
{"entry_id": "nMluoL5Z7jnTIq4Tjp_RgA", "businessname": "Mère Catherine", "address": "Nägelihof 3, 8001 Zürich"}
{"entry_id": "aR3Y2bYC5D5RVrLF-HhxlA", "businessname": "Café Odno", "address": "Kreuzstrasse 26, 8008 Zürich"}
{"entry_id": "VdhiHcfkVU2DzGZXbl_mKw", "businessname": "Enzian Cafébar Main Tower", "address": "Thurgauerstrasse 36, 8050 Zürich"}
{"entry_id": "jw62SZCUzDMUwuinnpY7hw", "businessname": "Burger King", "address": "Niederdorfstrasse 30, 8001 Zürich"}
{"entry_id": "ldZEiJRavmI_z3T1KNy80Q", "businessname": "Shinwazen", "address": "Freischützgasse 10, 8004 Zürich"}
{"entry_id": "adetcCrdgW5oB2OWoWOKrQ", "businessname": "Don Quijote", "address": "Brauerstrasse 36, 8004 Zürich"}
{"entry_id": "BN5dwXTZ8G1lOXilwHtApA", "businessname": "EAT.ch GmbH", "address": "Manessestrasse 85, 8045 Zürich"}
{"entry_id": "ySUAP9_-A42vuQZSvDtR6w", "businessname": "Cheti's Curry", "address": "Seefeldstrasse 7, 8008 Zürich"}
{"entry_id": "xNnGmtfex_kqeo4TX4g31Q", "businessname": "Ristorante Napoli", "address": "Sandstrasse 7, 8003 Zürich"}
{"entry_id": "6rU96lpXhSsGWfY8TTvNDQ", "businessname": "Küchenwerkstatt", "address": "Oberdorfstrasse 22, 8001 Zürich"}
{"entry_id": "8_bWr7 3tjEHrLq2WsIpWHw", "businessname": "Ristorante Totò", "address": "Seefeldstrasse 124, 8008 Zürich"}
{"entry_id": "5AcOgkWzPtMCZCA_nUfeOg", "businessname": "Tokyo Tapas", "address": "Zwinglistrasse 3, 8004 Zürich"}
{"entry_id": "gtGxEOa6b6yn2wtorMhlFg", "businessname": "Ristorante Vallocaia", "address": "Niederdorfstrasse 15, 8001 Zürich"}
{"entry_id": "HTkrD9qpZrdZD12_9tssKg", "businessname": "Canzoniere", "address": "Kanzleistrasse 84, 8004 Zürich"}
{"entry_id": "ovqHcxd1j1tAfpmJHRYOrg", "businessname": "THE YARD Restaurant & Hotel", "address": "Bäckerstrasse 62, 8004 Zürich"}
{"entry_id": "auVJlp4bhGSHrjf9IdjUoQ", "businessname": "Bar 63 GmbH", "address": "Rolandstrasse 19, 8004 Zürich"}
{"entry_id": "qkDt0q6EcjjBl6izn9BUOA", "businessname": "Restaurant Hirschen Serhan Safran", "address": "Waldstrasse 9, 8046 Zürich"}
{"entry_id": "V399T8wwL9xOub-_cUI1FQ", "businessname": "YOYO Pizza", "address": "Friesenbergstrasse 12, 8055 Zürich"}
{"entry_id": "xfX9KLfqOwtc5qZr0mncBg", "businessname": "Liquid-Bar", "address": "Zwinglistrasse 12, 8004 Zürich"}
{"entry_id": "g02HKKVdWsmf_LVnIiMAfA", "businessname": "Restaurant Jägerburg", "address": "Molkenstrasse 20, 8004 Zürich"}
{"entry_id": "9ihqYKLAXMg0KKj8b0WZwQ", "businessname": "Gül", "address": "Tellstrasse 22, 8004 Zürich"}
{"entry_id": "oVEjsPgiwXS-c2KqeO0FaA", "businessname": "blindekuh", "address": "Mühlebachstrasse 148, 8008 Zürich"}
{"entry_id": "rPs42JlyMK6zuDlCzLm1MA", "businessname": "Restaurant Milano", "address": "Militärstrasse 109, 8004 Zürich"}
{"entry_id": "nK9tVWe6dw14uf6lALSxKg", "businessname": "Casco Viejo", "address": "Rosengasse 7, 8001 Zürich"}
{"entry_id": "KCE9CC9se8RCv9M3Izutyw", "businessname": "Yalda Sihlcity", "address": "Kalanderplatz 1, 8045 Zürich"}
{"entry_id": "_o5FfFWQvqTdXsbZGsCzmA", "businessname": "Take Away-Pizza Sihlpassage", "address": "Passage Sihlquai, 8004 Zürich"}
{"entry_id": "Pf7515oobiyFDV63ff_vgA", "businessname": "Bistro Kafi", "address": "Stauffacherstrasse 141, 8004 Zürich"}
{"entry_id": "nQAdxmbPfr4rzoFgWE15Eg", "businessname": "Bistro Horizont", "address": "Mühlebachstrasse 112, 8008 Zürich"}
{"entry_id": "usbo-rCtqgCqg7orAwFBHg", "businessname": "dieci Gelateria & Take Away", "address": "Niederdorfstrasse 40, 8001 Zürich"}
{"entry_id": "4qaTdBE46YdFOtjPr2_DEQ", "businessname": "Veganitas Restaurant", "address": "Brauerstrasse 30, 8004 Zürich"}
{"entry_id": "-908eq4-ve5VXghCFHXxOg", "businessname": "WonderWaffel & Coffee Zürich", "address": "Seefeldstrasse 40, 8008 Zürich"}
{"entry_id": "Ljf4h79bF0w712-1K1eOPQ", "businessname": "Toro Bar", "address": "Schöneggstrasse 25, 8004 Zürich"}
{"entry_id": "Ky5_rAIEEqxV_-oi-galGg", "businessname": "Art 4 Bar - Music & Lounge", "address": "Kanonengasse 15, 8004 Zürich"}
{"entry_id": "uHLb0JLUfhYgM8JWVlgcVw", "businessname": "Cafeteria Bar-A-Graph", "address": "Badenerstrasse 90, 8004 Zürich"}
{"entry_id": "M47T9QxIgcsw0KgnZR6ZpQ", "businessname": "YALDA Europaallee", "address": "Gustav-Gull-Platz 2, 8004 Zürich"}
{"entry_id": "_kHybsmrFbi5Aub_2v5m3Q", "businessname": "Bäckerei Urs Vohdin", "address": "Oberdorfstrasse 12, 8001 Zürich"}
{"entry_id": "X6-6GqDtUkshhqetEE8_kQ", "businessname": "Igniv Zurich by Andreas Caminada", "address": "Marktgasse 17, 8001 Zürich"}
{"entry_id": "g0CGeMCH3xlhIB_3RQ0U8g", "businessname": "Shinwazen", "address": "Freischützgasse 10, 8004 Zürich"}
{"entry_id": "ptk6N1ex9Iyr_7tZI_2h3w", "businessname": "EGE Import & Export GmbH", "address": "Feldstrasse 133, 8004 Zürich"}
{"entry_id": "fjCnReANp7u9XOqq7Kpw1g", "businessname": "Sultan Sofrasi", "address": "Wehntalerstrasse 280, 8046 Zürich"}
{"entry_id": "HCXHXqM7erqTa8QXksfiPQ", "businessname": "Tiffins", "address": "Seefeldstrasse 61, 8008 Zürich"}
{"entry_id": "3xfEXKuxGS8FAvwrTxzgiw", "businessname": "Thai Heaven", "address": "Stüssihofstatt 3, 8001 Zürich"}
{"entry_id": "JMVQHZUDsbH_Y5WcNQ1FYQ", "businessname": "Restaurant Rechberg 1837", "address": "Chorgasse 20, 8001 Zürich"}
{"entry_id": "HWfhJncADRkaVrGNgzYvfQ", "businessname": "Restaurant Chez Dannys", "address": "Anemonenstrasse, 8047 Zürich"}
{"entry_id": "PxwPSUGWSjsCHEdlvVuhCA", "businessname": "yume-ramen gmbh", "address": "Reitergasse 6, 8004 Zürich"}
{"entry_id": "UKwPcbc3XUJdzGNCiLANmg", "businessname": "NZZ Café", "address": "Dock A 2472, 8060 Zürich"}
{"entry_id": "8cYIDy3G2YdO0CptIloEkQ", "businessname": "Pizza Restaurant Rosa", "address": "Birmensdorferstrasse 249, 8055 Zürich"}
{"entry_id": "jmHXZNXCHm0Y0twX2v8Udw", "businessname": "Family Grill GmbH", "address": "Bahnhaldenstrasse 2a, 8052 Zürich"}
{"entry_id": "2l2sfrjRGrwkTAsaF_dHHA", "businessname": "Limmathof", "address": "Limmatstrasse 217, 8005 Zürich"}
{"entry_id": "7GnxlaYYCJQbyZYuEPlUZQ", "businessname": "Ona Poké", "address": "Bleicherweg 19, 8002 Zürich"}
{"entry_id": "0mY2oqm3pSf6gXctSk10Hg", "businessname": "Ristorante Pizzeria Tramblu", "address": "Bucheggstrasse 103, 8057 Zürich"}
{"entry_id": "Qh87cFuRbqgG70GApIGgEA", "businessname": "Restaurant Emilio Weinhandlung AG", "address": "Zweierstrasse 9, 8004 Zürich"}
{"entry_id": "C0BRR7JRc6hICrjhDykWxw", "businessname": "Café Z am Park", "address": "Zurlindenstrasse 275, 8003 Zürich"}
{"entry_id": "9ioi08AZWL9wC-dqoocM2Q", "businessname": "Restaurant Römerblick", "address": "Asylstrasse 58, 8032 Zürich"}
{"entry_id": "SCabBm-sowavrRGV6lALhQ", "businessname": "Salir", "address": "Hottingerstrasse 27, 8032 Zürich"}
{"entry_id": "iNNcM1MgpXZG7WLY8bMHeQ", "businessname": "Delhihouse Of Be stcurry Restaurant", "address": "Zypressenstrasse 52, 8004 Zürich"}
{"entry_id": "EOtLvWO5D-7yMI4za4ozDg", "businessname": "Il Grappolo", "address": "Widmerstrasse 64, 8038 Zürich"}
{"entry_id": "Sl4SXhwDmePPNBlY6eBaPw", "businessname": "Maiden Shanghai Zurich", "address": "Döltschiweg 234, 8055 Zürich"}
{"entry_id": "0bW684mEAoK3oYlI2ctNsw", "businessname": "Kafi Linde", "address": "Bachstrasse 10, 8038 Zürich"}
{"entry_id": "15xDm2BA-0qaCB3QH7_gBA", "businessname": "Restaurant Grünwald", "address": "Regensdorferstrasse 237, 8049 Zürich"}
{"entry_id": "62gbz57eXz5y8rb3RkR69A", "businessname": "Cafeteria UZH Tierspital", "address": "Winterthurerstrasse 260, 8057 Zürich"}
{"entry_id": "HlgVa7CYjnwAh8Xj9ShJ0w", "businessname": "Si o No", "address": "Ankerstrasse 6, 8004 Zürich"}
{"entry_id": "lSZqJGOSyZRAYPzkuq53CQ", "businessname": "GRAND CAFÉ LOCHERGUT", "address": "Badenerstrasse 230, 8004 Zürich"}
{"entry_id": "6qQzgrx_ewihPHrGhuuKcA", "businessname": "Silberkugel:", "address": "Franklinstrasse 11, 8050 Zürich"}
{"entry_id": "s3A2S7NmncexNOdCM1gdqg", "businessname": "ApéRoyal GmbH", "address": "Tödistrasse 44, 8002 Zürich"}
{"entry_id": "XGoiUSdoNXaHG7en2z5IIg", "businessname": "Degenried Restaurant Wirtschaft", "address": "Degenriedstrasse 135, 8032 Zürich"}
{"entry_id": "jXCMlWFMuOgsMA8sNDqE3A", "businessname": "Monti's Bistro", "address": "Birmensdorferstrasse 486/488, 8055 Zürich"}
{"entry_id": "R1gtxd2fzcsnKaj3SEOvdg", "businessname": "Le Raymond Bar", "address": "Bleicherweg 8, 8001 Zürich"}
{"entry_id": "aFbc4kma5oZp0eyxbOSAGQ", "businessname": "Belcafé Pizza und Bar", "address": "Bellevueplatz 1, 8001 Zürich"}
{"entry_id": "GAKVBYPkbPFY-z0Hxws3uw", "businessname": "Restaurant Seerose", "address": "Seestrasse 493, 8038 Zürich"}
{"entry_id": "TkeCyV7tFHc_wafObM6Ebg", "businessname": "OYU Restaurant", "address": "Sihlstrasse 3, 8001 Zürich"}
{"entry_id": "rVcbO7l9-Qk24OiEzTjxog", "businessname": "Wühre Restaurant", "address": "Wühre 11, 8001 Zürich"}
{"entry_id": "J6RFpyVvZPj8mm02cWKdPQ", "businessname": "Hiltl Pflanzbar", "address": "Talstrasse 62, 8001 Zürich"}
{"entry_id": "yZ2tDMSfJ43eTmBGxhv7dA", "businessname": "Sala of Tokyo", "address": "Schützengasse 5, 8001 Zürich"}
{"entry_id": "vfd5yOh5xNcOvTGbUvGPtg", "businessname": "Napi‘s", "address": "Flurstrasse 4, 8048 Zürich"}
{"entry_id": "E3H1PB6YbgaqGFezZh1QgQ", "businessname": "GIESSEREI OERLIKON", "address": "Birchstrasse 108, 8050 Zürich"}
{"entry_id": "36diWUfVGP9cnv6_WARLKg", "businessname": "Kraftwerk", "address": "Selnaustrasse 25, 8001 Zürich"}
{"entry_id": "pzZSuui-6iK0T5lCFdTcMQ", "businessname": "Restaurant Sonne Libanon", "address": "Altstetterstrasse 223, 8048 Zürich"}
{"entry_id": "lvJxzKgsRKg06T1uLkSolQ", "businessname": "VIOR Zürich", "address": "Löwenstrasse 2, 8001 Zürich"}
{"entry_id": "CiUwUquR8ipFGZLzsihjjg", "businessname": "Globus Bellevue", "address": "Theaterstrasse 12, 8001 Zürich"}
{"entry_id": "XjuGFvMaRhDiLcBF_p9Mlg", "businessname": "Shilla", "address": "Badenerstrasse 505, 8048 Zürich"}
{"entry_id": "RJhTOnZ75lFFl0lMZTNlaw", "businessname": "Paninoteca La Penisola", "address": "Giessereistrasse 18, 8005 Zürich"}
{"entry_id": "97YU_Ll24wbtYgJyoSKs_w", "businessname": "Confiserie Cafe Bauer", "address": "Badenerstrasse 355, 8003 Zürich"}
{"entry_id": "41hM3ZuJHIevoqEbEGSZCw", "businessname": "Ristorante Klingler's", "address": "Münzplatz 3, 8001 Zürich"}
{"entry_id": "zOVQdAlNAed86Yheh6wIAw", "businessname": "Storchen Zürich", "address": "Weinplatz 2, 8001 Zürich"}
{"entry_id": "OjL-lmig51PmGHhL8xEdXQ", "businessname": "Restaurant Lunch 5 GmbH", "address": "Förrlibuckstrasse 62, 8005 Zürich"}
{"entry_id": "R2WIIn_pm5F9d6RFIu_EsA", "businessname": "Gerold Chuchi", "address": "Geroldstrasse 5, 8005 Zürich"}
{"entry_id": "45Nzv0t5R8y0k26QticFpw", "businessname": "Tibetasia", "address": "Quellenstrasse 6, 8005 Zürich"}
{"entry_id": "JCbPG1BpxPmJDumdI6o9kA", "businessname": "Bar Mau", "address": "Zypressenstrasse 36, 8003 Zürich"}
{"entry_id": "5K8ymGWuJ6dVjDxSpHlNIA", "businessname": "Pascals Diner", "address": "Bahnhofstrasse 1, 8001 Zürich"}
{"entry_id": "gca2BLQSsoUJSw6tO5f7Jw", "businessname": "Long Huang", "address": "Talstrasse 83, 8001 Zürich"}
{"entry_id": "80t2V0TEVXGmgPadwYKglg", "businessname": "Ali Baba", "address": "Josefstrasse 91, 8005 Zürich"}
{"entry_id": "ri9WOIWVPYmxa3Xn1eb5vw", "businessname": "Snack New Point", "address": "Langstrasse 206, 8005 Zürich"}
{"entry_id": "KvZ085B0lyCuyKHFk6TI2Q", "businessname": "Restaurant Lotus Garden", "address": "Waffenplatzstrasse 1, 8002 Zürich"}
{"entry_id": "ue0McHK6_Azww1e0XCvGpw", "businessname": "PURO - The Social Club", "address": "Fraumünsterstrasse 25, 8001 Zürich"}
{"entry_id": "lcQRtfxfWcr6uUEdHZglGw", "businessname": "Fleming's Club", "address": "Brandschenkestrasse 10, 8001 Zürich"}
{"entry_id": "QDeZvsAw-ZGNEMw_6PADbw", "businessname": "Ristorante Bindella", "address": "In Gassen 6, 8001 Zürich"}
{"entry_id": "O2y_gajTMINoI6R1WpWrgQ", "businessname": "Widder Restaurant", "address": "Widdergasse 6, 8001 Zürich"}
{"entry_id": "KBioOo0mUQ6Rabjr9Ib0jw", "businessname": "Starbucks Coffee", "address": "Rennweg 48, 8001 Zürich"}
{"entry_id": "swz8pt6-7g8It4bn9EIx-g", "businessname": "Churrasco", "address": "Glockengasse 9, 8001 Zürich"}
{"entry_id": "K8z4Qzng40UH9HhM6jVDeg", "businessname": "Lady Hamilton's Pub", "address": "Beatengasse 11, 8001 Zürich"}
{"entry_id": "rto1WU-zHv1TtgO4nfDg5g", "businessname": "Allegrotto", "address": "Bederstrasse 102, 8002  Zürich"}
{"entry_id": "KYyD1NaNA9Dk6P7d06lvyg", "businessname": "Indian BBQ Restaurant & Bar", "address": "Breitensteinstrasse 21, 8037 Zürich"}
{"entry_id": "juzho95er8Idnep0oU_OwQ", "businessname": "Wüscht Beckerei-Konditorei-Confiseri 8041 Leimbach", "address": "Maneggstrasse 73, 8041 Zürich"}
{"entry_id": "r5L4QXjM13efMiQp-hZYPQ", "businessname": "Michel Frey Landschaftsarchitekten GmbH", "address": "Allmendstrasse 100, 8041 Zürich"}
{"entry_id": "iB5WsHKkug1reDzwomWIDw", "businessname": "Sultanhan", "address": "Döltschihalde 31, 8055 Zürich"}
{"entry_id": "cf_0UnewV4IrxMmfrxnarA", "businessname": "Fries Brothers", "address": "Langstrasse 238, 8005 Zürich"}
{"entry_id": "Qc8aLFk26P-t1nDCmOeGoQ", "businessname": "Dunkin' Donuts", "address": "8001 Zürich"}
{"entry_id": "39-FuyYTI-DrK4_6AZrx_Q", "businessname": "Lima bar Zurich", "address": "Talacker 34, 8001 Zürich"}
{"entry_id": "EwcLUydWMWS9W0CYdOtifw", "businessname": "Restaurant Konshi", "address": "Uraniastrasse 3, 8001 Zürich"}
{"entry_id": "ed3ZrBUUtRoMrynjoyfxGQ", "businessname": "Chiantiquelle", "address": "Stampfenbachstrasse 38, 8006 Zürich"}
{"entry_id": "qybKuTS8vV4fhp4UZteAag", "businessname": "Thali Indian Restaurant", "address": "Schaffhauserstrasse 32, 8006 Zürich"}
{"entry_id": "uWgSDTmFN5Zqp9qgV9b3QQ", "businessname": "Dont Worry Eat Curry GmbH", "address": "Mattengasse 29, 8005 Zürich"}
{"entry_id": "_ENt6NS4KxaoHC3b_LuyTw", "businessname": "Aperobar Freude", "address": "Limmatstrasse 254, 8005 Zürich"}
{"entry_id": "eyr1oDANRUZclZILVnNtcw", "businessname": "D-Vino Weinbars AG", "address": "Schützengasse 12, 8001 Zürich"}
{"entry_id": "Rg3Hqs_zciXmjJF0V3Wx6g", "businessname": "Linde Oberstrass", "address": "Universitätstrasse 91, 8006 Zürich"}
{"entry_id": "Dm2QRk6Vsd3G-DjO-yLEWg", "businessname": "Skebe", "address": "St. Urbangasse 4, 8001 Zürich"}
{"entry_id": "2nSn6EaRx1g-s3Dta639GA", "businessname": "Saltinbocca", "address": "Viaduktstrasse 52, 8005 Zürich"}
{"entry_id": "DCR9CqIIFZJ6-gmyq3mcMw", "businessname": "Hausammann", "address": "Universitätstrasse 88, 8006 Zürich"}
{"entry_id": "BOHriit73-iLj5T6uAKEiA", "businessname": "Scent of Bamboo", "address": "8001 Zürich"}
{"entry_id": "G26xaGZkLHDaWNecqfbX_Q", "businessname": "Orsini", "address": "Waaggasse 7, 8001 Zürich"}
{"entry_id": "i7_QjUHgvieUec4aC9a47Q", "businessname": "Millennium", "address": "Limmatplatz 1, 8005 Zürich"}
{"entry_id": "K-7GD-Yf_SOtxzcEiD3UCQ", "businessname": "MIKI Ramen", "address": "Sihlfeldstrasse 63, 8003 Zürich"}
{"entry_id": "rt8K0_GbXeR4Pccci1F3QQ", "businessname": "Pery", "address": "Zentralstrasse 36, 8003 Zürich"}
{"entry_id": "ULXzywmZFPnbszfCJAdFtg", "businessname": "Dalou", "address": "Viaduktstrasse 93, 8005 Zürich"}
{"entry_id": "HHgZIuD8MxwZJCRBYVKkHw", "businessname": "Aroy Food GmbH", "address": "Hohlstrasse 556, 8048 Zürich"}
{"entry_id": "2kMCNz8GsMguPP70chIo9w", "businessname": "Willy's Fried Chicken", "address": "Badenerstrasse 540, 8048 Zürich"}
{"entry_id": "Dxq3wjp8oUNzuaRORQVqOA", "businessname": "Sterne Foifi", "address": "Theaterstrasse 22, 8001 Zürich"}
{"entry_id": "HQLyDwPlS64e6rYh8xrN6A", "businessname": "Bamboo Inn", "address": "Culmannstrasse 19, 8006 Zürich"}
{"entry_id": "57XPzv-WhB_VNXUHYpZzlA", "businessname": "Central Shisha Lounge", "address": "Stampfenbachstrasse 24, 8001 Zürich"}
{"entry_id": "i6OdEQxw4n3u2Cd9WKJZoQ", "businessname": "Bar Basso", "address": "Sihlstrasse 59, 8001 Zürich"}
{"entry_id": "s0he8ZshCEcp70E3GrP_dg", "businessname": "CLOUDS", "address": "Maagplatz 5, 8005 Zürich"}
{"entry_id": "DkvvZjobwMsSG5kPES6EnQ", "businessname": "Restaurant Co Chin Chin", "address": "Gasometerstrasse 7, 8005 Zürich"}
{"entry_id": "IBb7mpHGnJDu2qCw7kk5GA", "businessname": "Santa Lucia Limmatplatz", "address": "Luisenstrasse 31, 8005 Zürich"}
{"entry_id": "BsdnLjzF3ZvAEoR9gcZl2g", "businessname": "Restaurant Stapferstube Da Rizzo", "address": "Culmannstrasse 45, 8006 Zürich"}
{"entry_id": "_O0MTaYK-C4paHqtEIrVlg", "businessname": "Restaurant La Soupière", "address": "Bahnhofplatz 7, 8001 Zürich"}
{"entry_id": "KsCc4QRzmXBlmXw_jq-ljg", "businessname": "Yooji's Bellevue", "address": "St. Urbangasse 8, 8001 Zürich"}
{"entry_id": "6eCt9rt1_BPVv1yzmWcnFw", "businessname": "MyLocalina Showcase", "address": "Förrlibuckstrasse 62, 8005 Zürich"}
{"entry_id": "OBLZd1vAuWnCrte92zCsUg", "businessname": "Theater 11", "address": "Thurgauerstrasse 7, 8050 Zürich"}
{"entry_id": "fAYtAPHyMjByfRlrVRe2eg", "businessname": "Negishi Sushi x Bento, Zürich Oerlikon", "address": "Hofwiesenstrasse 363, 8050 Zürich"}
{"entry_id": "aianc5HIA-lbqQE_wAoWZg", "businessname": "Café Glättli", "address": "Glättlistrasse 40, 8048 Zürich"}
{"entry_id": "QDVJcbD3oq3-ua_ue0e1tA", "businessname": "Franco Pizza Kurier Zürich", "address": "Wattstrasse 7, 8050 Zürich"}
{"entry_id": "JqQmjYR50DOBzaJ3BMiVlg", "businessname": "Bagelboys Restaurant & Bakery", "address": "Dialogweg 11, 8050 Zürich"}
{"entry_id": "7hacxjZlOZV8gdtVvyj_ow", "businessname": "Bäckerei-Konditorei Stocker", "address": "Weinbergstrasse 93, 8006 Zürich"}
{"entry_id": "sQYdgeu7YSlAUAA8auhTCg", "businessname": "Restaurant Dorflinde", "address": "Schwamendingenstrasse 37, 8050 Zürich"}
{"entry_id": "MOBT_12YTde-9GicMA-IWw", "businessname": "Pizzeria Furetto", "address": "Wallisellenstrasse 5, 8050 Zürich"}
{"entry_id": "v0JEaAX5m4PoQ7D8rnE0eA", "businessname": "MediterRana", "address": "Albisstrasse 81, 8038 Zürich"}
{"entry_id": "k7WemTP31nUCgR6kWPv-cw", "businessname": "dean & david  franchise GmbH", "address": "Ernst-Nobs-Platz 1, 8004 Zürich"}
{"entry_id": "yDB5wcMCCjh8CghjYFy0AQ", "businessname": "Restaurant Weisses Kreuz", "address": "Falkenstrasse 27, 8008 Zürich"}
{"entry_id": "b54pGs6KtRKt9aq-JyAoKA", "businessname": "Restaurant Sorrento", "address": "Forchstrasse 2, 8008 Zürich"}
{"entry_id": "w_oVNai7R2xqIzf_si3IUw", "businessname": "Chez Oskar - Bowls & Sandwiches", "address": "Hohlstrasse 485, 8048 Zürich"}
{"entry_id": "-mr-VmD5Gx36ZCiMqotBvw", "businessname": "Domino's Pizza", "address": "Hohlstrasse 502, 8048 Zürich"}
{"entry_id": "e4ssBg5MxW6AUSSQ28A4tA", "businessname": "Olif Restaurant", "address": "Langstrasse 81, 8004 Zürich"}
{"entry_id": "EhMFl031wt0vWXot6o40Vg", "businessname": "Confiseur Bachmann AG", "address": "Kalanderplatz 1, 8045 Zürich"}
{"entry_id": "b4BY5xsWWAn0gWZRrACCvQ", "businessname": "El Mechoui", "address": "Niederdorfstrasse 31, 8001 Zürich"}
{"entry_id": "q8w4hBx-lBRXgiOxLk-KRQ", "businessname": "maritza", "address": "Schaffhauserstrasse 473, 8052 Zürich"}
{"entry_id": "X-T3GWFwaZL-DIaQly5tHg", "businessname": "Rheinfelder Bierhaus", "address": "Marktgasse 19, 8001 Zürich"}
{"entry_id": "J-2QaxP7j1GtLdYO-pAGyg", "businessname": "La Taqueria", "address": "Badenerstrasse 138, 8004 Zürich"}
{"entry_id": "01lRRd9d8Q9dmAbFEUlgNQ", "businessname": "Zum Husli", "address": "Risweg 1, 8041 Zürich"}
{"entry_id": "THJw27Fe662BGQOEbbZ-6w", "businessname": "Petite Madinina", "address": "Leutschenbachstrasse 52, 8050 Zürich"}
{"entry_id": "liL5SaNEYzIEFY5mRGsJpw", "businessname": "Pizzeria La Rustica", "address": "Schaffhauserstrasse 453, 8052 Zürich"}
{"entry_id": "eCl-bjY6i-VfRquHVVhMRA", "businessname": "Hirschen", "address": "Niederdorfstrasse 13, 8001 Zürich"}
{"entry_id": "fh09cdkBX6YLU_FZzS82mg", "businessname": "Saftlade", "address": "Münstergasse 31, 8001 Zürich"}
{"entry_id": "W0RKoHJvV5dXLkgMzUwymw", "businessname": "Cooperativo, Coopi", "address": "St. Jakobstrasse 6, 8004 Zürich"}
{"entry_id": "CNN8y_TwuPxUQ6LMd03PFg", "businessname": "Ristorante Pizzeria Chianalea", "address": "Brauerstrasse 87, 8004 Zürich"}
{"entry_id": "sr7ybMsthgTWKfjzfteUpQ", "businessname": "Starbucks", "address": "Limmatquai 144, 8001 Zürich"}
{"entry_id": "FJ-tf9pzs5aXAWLzbQ8kXQ", "businessname": "Shiso Burger Zurich", "address": "Weite Gasse 6, 8001 Zürich"}
{"entry_id": "fkDtptO9al5rsFUlsoI5JQ", "businessname": "Restaurant Blume", "address": "Winterthurerstrasse 534, 8051 Zürich"}
{"entry_id": "8LLcPkq0kcN4nC12m4SbnQ", "businessname": "Pizza Bonjour", "address": "Hagenholzstrasse 102, 8050 Zürich"}
{"entry_id": "OlH-v9sR2in6sYBSqh2cNQ", "businessname": "Osteria Sazio", "address": "Seefeldstrasse 27, 8008 Zürich"}
{"entry_id": "qQ0SdAnVQpuSxctiDRqCsA", "businessname": "DANTE a Bar and a Basement", "address": "Zwinglistrasse 22, 8004 Zürich"}
{"entry_id": "_-uRjVZkC1rA0OxxTj8axA", "businessname": "The Sacred mit Vegelateria", "address": "Muellerstrasse 64, 8004 Zürich"}
{"entry_id": "2QS9vfiIUjCoGsBZuhA-WQ", "businessname": "Zum weissen Kreuz", "address": "Rössligasse 3, 8001 Zürich"}
{"entry_id": "gTS4YA7fac0_boDpeEZ3gQ", "businessname": "Mövenpick Wein Schweiz AG", "address": "8001 Zürich"}
{"entry_id": "RM4CcKCVOnwkMldQqlIXLQ", "businessname": "SUBWAY Restaurant", "address": "Stauffacherstrasse 101, 8004 Zürich"}
{"entry_id": "dHOH14CGXit1j0Gh0Hzb4A", "businessname": "Goodys Smashburger", "address": "Mühlegasse 5, 8001 Zürich"}
{"entry_id": "cF0xQzL7CGZ06-_nK88ioA", "businessname": "HongKong Food Paradise", "address": "Kalandergasse 4, 8045 Zürich"}
{"entry_id": "y6BDupfg5irv2aM7Wwsg6w", "businessname": "Wirtschaft zur Au", "address": "Manessestrasse 208, 8045 Zürich"}
{"entry_id": "ESsvxXUypeXDO-EQD4jORw", "businessname": "Restaurant Café Zähringer Genossenschaft", "address": "Zähringerplatz 11, 8001 Zürich"}
{"entry_id": "BacaAY0glq9dcJgzEYb7LQ", "businessname": "dieci Pizza Kurier Binz-Wollishofen", "address": "Eibenstrasse 24, 8045 Zürich"}
{"entry_id": "dptXvHaycuaQQqxg9mSnbw", "businessname": "Spanische Weinhalle", "address": "Münstergasse 15, 8001 Zürich"}
{"entry_id": "jQ85miH0_IOakyYWtMK6UA", "businessname": "Store Central", "address": "Limmatquai 144, 8001 Zürich"}
{"entry_id": "35Cn3GgynZxLRvf-SEHDdA", "businessname": "Weinbistro Karim", "address": "Zwinglistrasse 6, 8004 Zürich"}
{"entry_id": "DmvzYOhlPjegI0rNYWhK3A", "businessname": "Lindas Paradise", "address": "Zähringerstrasse 12, 8001 Zürich"}
{"entry_id": "pQM2ERptv2mPKtfP7_oKtg", "businessname": "Simon's Steakhouse Grill & Restaurant & Bar", "address": "Niederdorfstrasse 11, 8001 Zürich"}
{"entry_id": "e25ogdxkYgLPC8NFxo7NVA", "businessname": "Bierwerk Züri", "address": "Gustav-Gull-Platz 10, 8004 Zürich"}
{"entry_id": "nmmHoc55M-NODuMhntUC1A", "businessname": "Pizzeria Don Emillio", "address": "Dübendorfstrasse 24, 8051 Zürich"}
{"entry_id": "E-pGwVN236f7fC57O-41BA", "businessname": "Restaurant Opera", "address": "Dufourstrasse 2, 8008 Zürich"}
{"entry_id": "QLisN8ev675ufvogaD1nOg", "businessname": "Weinstube Limmathof", "address": "Limmatquai 142, 8001 Zürich"}
{"entry_id": "HCGWamtmdToVFzJ2HY7hFw", "businessname": "Napoli da Gerardo", "address": "Sandstrasse 7, 8003 Zürich"}
{"entry_id": "fXabBZwZIhTj4SI7DioJMg", "businessname": "Restaurant IKOO", "address": "Bäckerstrasse 37, 8004 Zürich"}
{"entry_id": "gwJmJzSB9P2mELuxxcTGog", "businessname": "Bonnie Prince Pub", "address": "Zähringerstrasse 38, 8001 Zürich"}
{"entry_id": "_6jAA4yIPQxpMvfA2UdkZw", "businessname": "Äss-Bar", "address": "Stüssihofstatt 6, 8001 Zürich"}
{"entry_id": "zT15jcX4liDKdeem0ee9Ag", "businessname": "Gelati Tellhof", "address": "Tellstrasse 20, 8004 Zürich"}
{"entry_id": "3q1qNKXcrs2PKZmQoEMwCg", "businessname": "Backhuus Fischer", "address": "Schaffhauserstrasse 520, 8052 Zürich"}
{"entry_id": "4ZQ57Cr1L9Y89iWbo6aAvQ", "businessname": "Gelati am See", "address": "Seefeldquai, 8008 Zürich"}
{"entry_id": "XhLc5Wr6_SKTQ0yBncgBNw", "businessname": "Starbucks", "address": "Europaallee 7, 8004 Zürich"}
{"entry_id": "L3_GfzNEreadDUM7gS2pkg", "businessname": "Bank", "address": "Molkenstrasse 15, 8004 Zürich"}
{"entry_id": "bI2vbX0Hi7mIW-j_CDHXog", "businessname": "Omnia Coffee", "address": "Stauffacherstrasse 105, 8004 Zürich"}
{"entry_id": "XnFFGMKCMki0MuSrRMG-Pw", "businessname": "L'ADORO Restaurant", "address": "Glatttalstrasse 104, 8052 Zürich"}
{"entry_id": "RmAEiKqczgx-pseRuGU1Aw", "businessname": "Walliser Keller im Niederdorf", "address": "Zähringerstrasse 21, 8001 Zürich"}
{"entry_id": "IfBIs3dFe-g3zDlVeX0-uA", "businessname": "La Penisola", "address": "Uetlibergstrasse 132, 8045 Zürich"}
{"entry_id": "AZSwcx4ebNCJ5jFtMSjm3A", "businessname": "Nooch Asian Kitchen Zürich Steinfels", "address": "Heinrichstrasse 267, 8005 Zürich"}
{"entry_id": "5gbR7h-hfAX6t8823IllHA", "businessname": "Ristorante Conti", "address": "Dufourstrasse 1, 8008 Zürich"}
{"entry_id": "D3CCwLrDitYBjWIgHWtTzg", "businessname": "Dieci gelato e caffè Limmatquai", "address": "Limmatquai 32, 8001 Zürich"}
{"entry_id": "sqPUq08Rj18m4Up2Om__kA", "businessname": "Joe & The Juice", "address": "Limmatquai 70, 8001 Zürich"}
{"entry_id": "b_Bevyz30YPcarOQclU72g", "businessname": "Le Chef Metas Restaurant", "address": "Kanonengasse 29, 8004 Zürich"}
{"entry_id": "xN8F1GIdWUS4EID4S8HBRg", "businessname": "Veltlinerkeller (ZURICH)", "address": "Schlüsselgasse 8, 8001 Zürich"}
{"entry_id": "lV5wxKJNP9rqM0yz2MoXqg", "businessname": "Café Piazza", "address": "Idaplatz 2, 8003 Zürich"}
{"entry_id": "C7CZHZxUqaADytceMBul2Q", "businessname": "Steakhouse Meat Me", "address": "Rebgasse 8, 8004 Zürich"}
{"entry_id": "FbZ5bKOU8_Cflkes02SnYQ", "businessname": "Kentucky Fried Chicken", "address": "Zürich Flughafen 3, 8060 Zürich"}
{"entry_id": "FpnIr6F92594C1Ex4vphTA", "businessname": "Châlet Suisse", "address": "8060 Zürich"}
{"entry_id": "W8gOPa6iyAVEGZUNaY0Jnw", "businessname": "Marche Bistro", "address": "8060 Zürich"}
{"entry_id": "CFZFwgZexEHz2453doREow", "businessname": "yámas gastro ag", "address": "Lagerstrasse 47, 8004 Zürich"}
{"entry_id": "v8QDcGIcLo8eJnF0ElP3dQ", "businessname": "Pizzeria Bella Napoli Zürich", "address": "Birmensdorferstrasse 249, 8055 Zürich"}
{"entry_id": "MgXZogLxptV6b1Oj0jNpKg", "businessname": "Casa Gourmet GmbH", "address": "Birmensdorferstrasse 259, 8055 Zürich"}
{"entry_id": "EY4n01GZRAdhX8LkkBMeXw", "businessname": "Papa Joe's", "address": "Schifflände 18, 8001 Zürich"}
{"entry_id": "gzqOIwxuof-6ldUTerTPcw", "businessname": "Beetnut Operations AG", "address": "Lagerstrasse 16b, 8004 Zürich"}
{"entry_id": "JuFXj4vGu5So98GSD9kfEg", "businessname": "Gate Gourmet", "address": "8058 Zürich"}
{"entry_id": "JUu_JaKK1GL8r3qShs6kTg", "businessname": "Ruen Thai By Suthita", "address": "General-Wille-Strasse 18, 8002 Zürich"}
{"entry_id": "LexZN_zctbFU-SJEo5Zl1A", "businessname": "Gasthaus ZUM GUTEN GLÜCK", "address": "Stationsstrasse 7, 8003 Zürich"}
{"entry_id": "X_OwTCne0l--KKVf6sfMew", "businessname": "La Pinseria", "address": "Hardplatz 9, 8004 Zürich"}
{"entry_id": "Qgd87S9TFN68lmPd7kFTLg", "businessname": "McDonald's Restaurant", "address": "Badenerstrasse 21, 8004 Zürich"}
{"entry_id": "Hczwpv0u-apSyhxdXMOkUQ", "businessname": "Jeunesse", "address": "Wehntalerstrasse 120, 8057 Zürich"}
{"entry_id": "pOrZfkR6XM8-ZoXYg3IJuw", "businessname": "Tune In", "address": "Döltschiweg 234, 8055 Zürich"}
{"entry_id": "aF-xIUpHgSOsoRM-QA73hw", "businessname": "New Point", "address": "Albisriederplatz 5, 8004 Zürich"}
{"entry_id": "fBI93egKuJ_plJhNSSc1nw", "businessname": "Bohemia", "address": "Klosbachstrasse 2, 8032 Zürich"}
{"entry_id": "VqRtTg_SUB1xm9SINulerw", "businessname": "Dal Sardo", "address": "Asylstrasse 60, 8032 Zürich"}
{"entry_id": "yQv0ny5ERRAsqz5dFt-kGQ", "businessname": "Barfly'z", "address": "Gotthardstrasse 21, 8002 Zürich"}
{"entry_id": "2iRYw6szGFEZWlVXMRfsDw", "businessname": "Vier Linden", "address": "Freiestrasse 50, 8032 Zürich"}
{"entry_id": "8fvrePtd-W_OAA2y1d_HWQ", "businessname": "Caffe Spettacolo", "address": "Tessinerplatz 10, 8002 Zürich"}
{"entry_id": "1u0DEdHCWJbWfMbo93mxIg", "businessname": "Miss Miu", "address": "Badenerstrasse 97, 8004 Zürich"}
{"entry_id": "xs2Tm_3Px0TMsvP2bai-pA", "businessname": "Confiserie St. Jakob", "address": "Badenerstrasse 41, 8004 Zürich"}
{"entry_id": "yMhDKQ7Pmpv_HTay8Mvdbg", "businessname": "Püente", "address": "Baumgasse 10, 8005 Zürich"}
{"entry_id": "N7ysflZdO8oRE3s-158bzg", "businessname": "Tacos Ramiro Y Macario", "address": "Hardstrasse 9, 8004 Zürich"}
{"entry_id": "A00OhenWd_Z5RWnxDE7mqA", "businessname": "localsearch (Swisscom Directories AG)", "address": "Förrlibuckstrasse 62, 8005 Zürich"}
{"entry_id": "M0BX41dEKt8oefn5GkNSgA", "businessname": "Casa Ferlin AG1", "address": "Förrlibuckstrasse 62, 8005 Zürich"}
{"entry_id": "Y_ylXDLP3fiaZvkHtYuV2A", "businessname": "Yalla Habibi", "address": "Meinrad-Lienert-Strasse 27, 8003 Zürich"}
{"entry_id": "yjUfGZW0D27lU7Pdt6b6Gw", "businessname": "Burgermeister Limmatplatz", "address": "Langstrasse 243, 80 05 Zürich"}
{"entry_id": "CmaTmK9uMGD5vTXQf19Cxw", "businessname": "The Vault Wine Bar", "address": "Döltschiweg 234, 8055 Zürich"}
{"entry_id": "VCYgt4-B32_Hb3QLmh9aRw", "businessname": "Corner 48", "address": "Stampfenbachplatz 4, 8006 Zürich"}
{"entry_id": "MR8B573IhpYDZhdd5DrM9g", "businessname": "Café Bar Nordbrücke", "address": "Dammstrasse 58, 8037 Zürich"}
{"entry_id": "TcCrSabId9XT6V22KOCuLg", "businessname": "Restaurant Damas", "address": "Josefstrasse 151, 8005 Zürich"}
{"entry_id": "Z-D1vZEcSaBB95yG1u3nXw", "businessname": "Zest of Asia", "address": "Luisenstrasse 43, 8005 Zürich"}
{"entry_id": "kzbJPQ9e-B17iVoope_F2w", "businessname": "SelnauWok GmbH", "address": "Selnaustrasse 5, 8001 Zürich"}
{"entry_id": "upjFSyGdQNfwQbz71rQ4SA", "businessname": "Residenz Restaurant", "address": "Spirgartenstrasse 2, 8048 Zürich"}
{"entry_id": "crORKanLMxXtanFeK8MakA", "businessname": "Takano City", "address": "Löwenstrasse 29, 8001 Zürich"}
{"entry_id": "EXh8YX7qKq-_J2cfUnDv6g", "businessname": "Sorell Hotel Seidenhof", "address": "Sihlstrasse 9, 8001 Zürich"}
{"entry_id": "AYJfVHKxzPuJ4hbZ6p8tYQ", "businessname": "Rice Up! Stadelhofen", "address": "Stadelhoferstrasse 18, 8001 Zürich"}
{"entry_id": "aJVsNPZorsROvZ9jHFXV4Q", "businessname": "Edomae", "address": "Talstrasse 62, 8001 Zürich"}
{"entry_id": "Pxc2twCUsZFjDXPT-jlJVg", "businessname": "azzurri", "address": "Badenerstrasse, 8048 Zürich"}
{"entry_id": "2wBHGPU6qpSfRwgD0ywBaw", "businessname": "Original Kebap House", "address": "Franklinstrasse 20, 8050 Zürich"}
{"entry_id": "ZhKyqPZi3Be-3Q0HVb449w", "businessname": "dieci Pizza Kurier Zürichberg", "address": "Landoltstrasse 7, 8006 Zürich"}
{"entry_id": "fECzgCHCby0yAay7n0fc8g", "businessname": "Best Kebab", "address": "Langstrasse 206, 8005 Zürich"}
{"entry_id": "KrNyru4gx4RAuozpHf23jA", "businessname": "Emma's Bakery", "address": "Schaffhauserstrasse 125, 8057 Zürich"}
{"entry_id": "ve1094FSlT8PCZbLrFtb1Q", "businessname": "Rest. Kornhaus", "address": "Langstrasse 243, 8005 Zürich"}
{"entry_id": "eKkt6ycatSv5r5NlTWnkQw", "businessname": "Famiglia Tremonte", "address": "Birmensdorferstrasse 129, 8003 Zürich"}
{"entry_id": "gAVeB2esapc9QShAV6IIZw", "businessname": "Restaurant & Pizzeria da Angelo", "address": "Badenerstrasse 275, 8003 Zürich"}
{"entry_id": "3lLSAV26ZQunER0HNjL3UQ", "businessname": "Walhalla Hotel", "address": "Limmatstrasse 5, 8005 Zürich"}
{"entry_id": "GQZtd69tqdnhrc0_GYJdpA", "businessname": "Brasserie Spirgarten", "address": "Lindenplatz 5, 8048 Zürich"}
{"entry_id": "DYoDvMx8Dhh4mjTab5v1TQ", "businessname": "First Base Afrofood", "address": "Badenerstrasse 276, 8004 Zürich"}
{"entry_id": "DB6A3EY7fxk3y670buc2og", "businessname": "Nadas", "address": "Bederstrasse 77, 8002 Zürich"}
{"entry_id": "-5O2nEiAxGiAVphjOH7ZSA", "businessname": "Kian", "address": "Stampfenbachstrasse 24, 8001 Zürich"}
{"entry_id": "b9feuEikUQmFIU7MLR8a1Q", "businessname": "Il Baretto Josef", "address": "Josefstrasse 13, 8005 Zürich"}
{"entry_id": "WGZV3glDJp1BKZUzy4CAyA", "businessname": "Micas Garten", "address": "Badenerstrasse 790, 8048 Zürich"}
{"entry_id": "RzF8WsDlBxgtl4nBRNSCwg", "businessname": "Restaurant TESSIN GROTTO", "address": "Waidbadstrasse 151, 8037 Zürich"}
{"entry_id": "qgR4s1g_F-zs_CjCP7vi_w", "businessname": "Swiss Bistro", "address": "Schiffbaustrasse 11, 8005 Zürich"}
{"entry_id": "cSfn_ZAcycAebg_c6m4yLg", "businessname": "Commihalles", "address": "Stampfenbachstrasse 6, 8001 Zürich"}
{"entry_id": "e0vtQ7bTtXsVIP3-7Z9IFw", "businessname": "Burger Brothers GmbH", "address": "Altstetterstrasse 147, 8048 Zürich"}
{"entry_id": "fj7DXO926W8woe3yS6MvkQ", "businessname": "Marktlücke GmbH", "address": "Hermetschloostrasse 70, 8048 Zürich"}
{"entry_id": "M1oSki-mzf9tFQesNwcl6w", "businessname": "Thai Sun Garden", "address": "Winterthurerstrasse 281, 8057 Zürich"}
{"entry_id": "rHMNSf83nrncw9VvRKcPhg", "businessname": "BARADOX", "address": "Sihlstrasse 73, 8001 Zürich"}
{"entry_id": "5Zj9hWF1kzdPJz-RjaiHxw", "businessname": "Venice Bar", "address": "Schiffbaustrasse 4, 8005 Zürich"}
{"entry_id": "oGcoSoh6VKsOdNZLmHBHNQ", "businessname": "FAMO", "address": "Talstrasse 20, 8001 Zürich"}
{"entry_id": "JdN2Fgsg3L_LLlysFzh4xg", "businessname": "The Counter", "address": "Bahnhofplatz 15, 8001 Zürich"}
{"entry_id": "CgLebB9HJKgnBMj-WAchww", "businessname": "Caredda Paolo", "address": "Josefstrasse 119, 8005 Zürich"}
{"entry_id": "aQFj6FZ0lVMKO4rZc54NuA", "businessname": "Kaimug Altstetten", "address": "Altstetterstrasse 145, 8048 Zürich"}
{"entry_id": "lhILKmVD0vadCBAVD3Si0A", "businessname": "Walliser Kanne", "address": "Lintheschergasse 21, 8001 Zürich"}
{"entry_id": "fPAZBNzBQnCzM3yPd_2_Pw", "businessname": "Ristorante Toscano Im Puls 5", "address": "Giessereistrasse 18, 8005 Zürich"}
{"entry_id": "s1AVBrtUScVJYoIOMq7OMw", "businessname": "Restaurant La Terrasse", "address": "Badenerstrasse 537, 8048 Zürich"}
{"entry_id": "cVkcY-NwfGtw-rxMqkZX_Q", "businessname": "Grottino 83", "address": "Letzigraben 245, 8047 Zürich"}
{"entry_id": "saNqgMgsJMJCr8ekMsCjqg", "businessname": "Felix", "address": "Kalkbreitestrasse 8, 8003 Zürich"}
{"entry_id": "XaFc3_6wiFYrcPHLNdK2qw", "businessname": "Restaurant Schützenruh AG", "address": "Uetlibergstrasse 300, 8045 Zürich"}
{"entry_id": "Sk8YpPfHXre9i_RZxYyloA", "businessname": "Gastrolac Resto GmbH", "address": "Seestrasse 495, 8038 Zürich"}
{"entry_id": "Fdk-tdjPb91hA6slsv-cqw", "businessname": "China Restaurant", "address": "Tessinerplatz 12, 8002 Zürich"}
{"entry_id": "31lzOvK_ _8nVc1PQNGaxpA", "businessname": "Da Pizzi", "address": "Josefstrasse 27, 8005 Zürich"}
{"entry_id": "GCsfT-eoUU2G4FOiRmLAHg", "businessname": "FiveSpice Thai Restaurant", "address": "Zweierstrasse 106, 8003 Zürich"}
{"entry_id": "vrJIe9DWBPatVM0uFt5joA", "businessname": "Restaurant AXOi", "address": "Meinrad-Lienert-Strasse 23, 8003 Zürich"}
{"entry_id": "Y45CYqVkUy2awmjj3ZHBaQ", "businessname": "HUA THAI", "address": "Hardstrasse 320, 8005 Zürich"}
{"entry_id": "_TT36JeTjIAzvoEe81mnBA", "businessname": "Zumfondue", "address": "Museumstrasse 1, 8001 Zürich"}
{"entry_id": "6lt5x50m1TUn-elWEgCNsw", "businessname": "Cafeteria KS Stadelhofen", "address": "Promenadengasse 5, 8090 Zürich"}
{"entry_id": "LTUcznib4XbdYeZ95N-pGw", "businessname": "Osteria da Biagio", "address": "Limmattalstrasse 228, 8049 Zürich"}
{"entry_id": "KTEXUS_xsKDGY1LFrMqO1A", "businessname": "Osteria Centrale", "address": "Nordstrasse 205, 8037 Zürich"}
{"entry_id": "ZnwJMgWfiZhaTsuUJ-zeIA", "businessname": "Le Jardin", "address": "Stockerstrasse 17, 8002 Zürich"}
{"entry_id": "kiY78SwOqmqPLQlfgKAyMA", "businessname": "Nagasui AG", "address": "Selnaustrasse 16, 8001 Zürich"}
{"entry_id": "Slla1mzF6sr7UH5HucQeYQ", "businessname": "Pret A Manger Dock D", "address": "Postfach 2472, Bahnhofsterminal, Zürich Flughafen, 8060 Zürich"}
{"entry_id": "3PHK62yE89D9oIPEHMCfqA", "businessname": "'itos", "address": "Neymarstrasse 25, 8311 Zürich"}
{"entry_id": "vHL2TbutZ4U3wn_nuOfd8g", "businessname": "Restaurant La Côte", "address": "Aemtlerstrasse 26, 8003 Zürich"}
{"entry_id": "f3hKW0EULE8ixrM1MQPL4A", "businessname": "Cafeteria ZHdK Sihlquai", "address": "Sihlquai 87, 8005 Zürich"}
{"entry_id": "xDpY3FN3pv7_uC4TVMBUjA", "businessname": "EQUINOX Restaurant", "address": "Turbinenstrasse 20, 8005 Zürich"}
{"entry_id": "363f7XDw8zWJ-ZrfAwoVcw", "businessname": "Restauarant Grotto Reale", "address": "Martastrasse 145, 8003 Zürich"}
{"entry_id": "fNopuqCM3E7eQs1QoSjm6Q", "businessname": "Frau Gerolds Garten", "address": "Geroldstrasse 23A, 8005 Zürich"}
{"entry_id": "KTJg0pSXKWObC6qEptxFrQ", "businessname": "Burgermeister", "address": "Hardstrasse 316, 8005 Zürich"}
{"entry_id": "P1wwhkZR7aRcYdA1xsPnrA", "businessname": "Steiner Flughafebeck", "address": "Turbinenstrasse 22, 8005 Zürich"}
{"entry_id": "0FKms4RRfO5ZsVx187xENw", "businessname": "Old Fashion Bar AG", "address": "Fraumünsterstrasse 15, 8001 Zürich"}
{"entry_id": "rhoUejeL6HaKAAo490R3HA", "businessname": "Vis à Vis", "address": "Talstrasse 40, 8001 Zürich"}
{"entry_id": "dTMPpeLQLuNSA1JcYWu2yg", "businessname": "Kai Sushi Schiffbau Zürich", "address": "Hardstrasse 261, 8005 Zürich"}
{"entry_id": "Rvb8eYY6z9gBkdOqrG85Fg", "businessname": "La Pizza Buona", "address": "Altstetterstrasse 239, 8048 Zürich"}
{"entry_id": "VsUDF2vHreQEtErzBaI5WQ", "businessname": "SUC+ Juice Bars", "address": "8050 Zürich"}
{"entry_id": "qavb0cROXgYAN5Virf9PHw", "businessname": "Restaurant Löwen Siam", "address": "Baumackerstrasse 47, 8050 Zürich"}
{"entry_id": "VO6cOzcmf8GuACroVp_pBg", "businessname": "Restaurant Sonne Libanon", "address": "Altstetterstrasse 223, 8048 Zürich"}
{"entry_id": "CAQdmfSmTPcUjCPpVBO9wg", "businessname": "ATELIER BAR", "address": "Talacker 16, 8001 Zürich"}
{"entry_id": "0jL2QzXFj6y8KeVlQMTszw", "businessname": "McDonald's Restaurant", "address": "Hofwiesenstrasse 350-354, 8050 Zürich"}
{"entry_id": "jKzC1Qed4kQ5DZZzxZT9WA", "businessname": "SAIGON", "address": "Sihlstrasse 97, 8001 Zürich"}
{"entry_id": "renz3HWMUycJbXa9tcHU6w", "businessname": "Bärengasse Restaurant", "address": "Bahnhofstrasse 25, 8001 Zürich"}
{"entry_id": "T-JSe1kssU6N8CmLH9D6HA", "businessname": "Ayverdi's Oerlikon", "address": "Genossenschaftsstrasse 18, 8050 Zürich"}
{"entry_id": "DgRbhGxaIrrFrIn1u50bsg", "businessname": "Williams ButchersTable Hegibachplatz", "address": "Neumünsterstrasse 34, 8008 Zürich"}
{"entry_id": "UXn6QLTrCIcW_kkdgogboA", "businessname": "Fusio", "address": "Max-Bill-Platz 15, 8050 Zürich"}
{"entry_id": "Tkcw2Nr8vlV0N-BQCM3rcQ", "businessname": "Ristorante Da Angela", "address": "Hohlstrasse 449, 8048 Zürich"}
{"entry_id": "y1rEUgTbk9VyjlntEZKWGQ", "businessname": "Brasserie La Pontaise", "address": "Krönleinstrasse 14, 8044 Zürich"}
{"entry_id": "IuSbePwsucAjJ4RnVclTBg", "businessname": "Samurai VII", "address": "Badenerstrasse 651, 8048 Zürich"}
{"entry_id": "T81EQsKXtNmqEtoHa6ux9A", "businessname": "eCHo", "address": "Neumühlequai 42, 8006 Zürich"}
{"entry_id": "ii-kdnOaA2h40KaVlxAuFQ", "businessname": "McDonald's Restaurant", "address": "Hohlstrasse 467, 8048 Zürich"}
{"entry_id": "HBg9EuSq2GFomwFrbelXKw", "businessname": "Hotel Glockenhof", "address": "Sihlstrasse 31, 8001 Zürich"}
{"entry_id": "20WIKrwBt2Rlu1J1XsHErw", "businessname": "tibits", "address": "Tramstrasse 2, 8050 Zürich"}
{"entry_id": "qLynStOJF6sC0F0ARLrFQw", "businessname": "Backerei Hug", "address": "Vulkanplatz 31, 8048 Zürich"}
{"entry_id": "ruS3buwBHFCWjdUcAQmgCg", "businessname": "AURA Group AG", "address": "Bleicherweg 5, 8001 Zürich"}
{"entry_id": "FHKO0L40ZXm_JSHux5-4jw", "businessname": "Café du Bonheur GmbH", "address": "Zypressenstrasse 115, 8004 Zürich"}
{"entry_id": "VQ7LWGF9Uk4scSHnczoJMA", "businessname": "Restaurant Börni's Baizli", "address": "Tramstrasse 17, 8050 Zürich"}
{"entry_id": "-sEHa5O0kT8zvPrJhZHjyA", "businessname": "Letzistübli", "address": "Albisriederstrasse 171, 8047 Zürich"}
{"entry_id": "E7mGnVU3wfRoxUrZv48fyg", "businessname": "Nikos Griechische Taverne", "address": "A lbisriederstrasse 181, 8047 Zürich"}
{"entry_id": "WTW_Ra_l0GfINlQ9lLoVvQ", "businessname": "50zu5", "address": "Zollikerstrasse 6, 8008 Zürich"}
{"entry_id": "lLl1wRlxvqDUOz4sOywVlw", "businessname": "LOFT FIVE", "address": "Europaallee 15, 8004 Zürich"}
{"entry_id": "-nATy3Z3uJl_Zoek70nOwQ", "businessname": "Spuntino", "address": "Bellerivestrasse 253, 8008 Zürich"}
{"entry_id": "AK_7BgSvo5jYS3rSy70qHA", "businessname": "Rheinfelder Bierhalle", "address": "Niederdorfstrasse 76, 8001 Zürich"}
{"entry_id": "51YVzr4DcPydBphOaeRUIw", "businessname": "Convivio", "address": "Rotwandstrasse 62, 8004 Zürich"}
{"entry_id": "NN-796mIiF4JvvkbyiTEHQ", "businessname": "Restaurant Tüfenegg", "address": "Dufourstrasse 154, 8008 Zürich"}
{"entry_id": "CX-H-vCICcS3uYw6XaR4ZQ", "businessname": "Habesha GmbH", "address": "Schreinerstrasse 64, 8004 Zürich"}
{"entry_id": "nM6t5qipJ8Oyl85e0vgCzQ", "businessname": "Brauerei Oerlikon AG", "address": "Schärenmoosstrasse 105, 8052 Zürich"}
{"entry_id": "8Cq_bQt-BZ-IsW7dI71FnA", "businessname": "Cèdre-Bellevue", "address": "Schifflände 5, 8001 Zürich"}
{"entry_id": "WBvoM3YGP2o12tYFzKs55w", "businessname": "Vohdin Urs", "address": "Oberdorfstrasse 12, 8001 Zürich"}
{"entry_id": "GRrAvcos-I0a251z0sVYMw", "businessname": "Kuhn Bäckerei Cafe", "address": "Leimbachstrasse 23, 8041 Zürich"}
{"entry_id": "pcG1TsJuXm4TGRDw48Hzsg", "businessname": "Restaurant Zeughaushof", "address": "Kanonengasse 20, 8004 Zürich"}
{"entry_id": "qnFV4hLSuTCwvkns2vmmxw", "businessname": "Celia", "address": "Langstrasse 35, 8004 Zürich"}
{"entry_id": "ow07qLETefBX83AppgtykQ", "businessname": "Restaurant Druckzentrum Bubenberg", "address": "Bubenbergstrasse 1, 8045 Zürich"}
{"entry_id": "xBuFdcWRc_zmWZQ9J2SbLw", "businessname": "Pizzeria Piazza", "address": "Wehntalerstrasse 546, 8046 Zürich"}
{"entry_id": "XgTc-SuFym6jqgvXhEoXFg", "businessname": "BarMünster", "address": "Münstergasse 30, 8001 Zürich"}
{"entry_id": "vnVHV4n8grH1HnO_WI6Pow", "businessname": "Don Leone", "address": "Bäckerstrasse 31, 8004 Zürich"}
{"entry_id": "Tpt2CKmMxyU4OgEN00xIRQ", "businessname": "Libanesisch Cèdre", "address": "Badenerstrasse 78, 8004 Zürich"}
{"entry_id": "vgHGNt2_8JUJf0GQk8IkMA", "businessname": "Masi Wine Bar & Restaurant", "address": "Seefeldstrasse 5, 8008 Zürich"}
{"entry_id": "78xMMLEcC4WtVY2byw72Pw", "businessname": "Restaurant Madrid", "address": "Froschaugasse 15, 8001 Zürich"}
{"entry_id": "t3IvATLsxkeYmo7WXI_iTw", "businessname": "Chinagarten Take Away", "address": "Bellerivestrasse 144, 8008 Zürich"}
{"entry_id": "mhDJ6LNUdEWMeshkhUPlbg", "businessname": "Restaurant La Zagra", "address": "Seefeldstrasse 273, 8008 Zürich"}
{"entry_id": "cv9xfPxAnHuxGyeED9VCfA", "businessname": "Restaurant Bar noon", "address": "Oberdorfstrasse 9, 8001 Zürich"}
{"entry_id": "Ko0CiFPwkmyRNsoYh6ZQCA", "businessname": "CS clube-social", "address": "Zeughaushof 3, 8004 Zürich"}
{"entry_id": "8Sx24OlrJxK0ONLDEBSUKQ", "businessname": "Hammam Basar AG", "address": "Mühlebachstrasse 155, 8008 Zürich"}
{"entry_id": "DC3yewmG9082XkPGiKv22A", "businessname": "La Lup, Asian Kitchen", "address": "Wolframplatz 1, 8045 Zürich"}
{"entry_id": "o0SbTqeqWnye2bWvwABtCA", "businessname": "Sushi Nation", "address": "Köschenrütistrasse 6, 8052 Zürich"}
{"entry_id": "djyNtpC1EsMVycK9vPsBCQ", "businessname": "Cafe Kornsilo", "address": "Seefeldstrasse 231, 8008 Zürich"}
{"entry_id": "OgeyfaL_tPQ8bM8a8q9ExA", "businessname": "Bar Zänker", "address": "Zähringerstrasse 39, 8001 Zürich"}
{"entry_id": "cMlIMWiMXulU9vnBQ7odvw", "businessname": "Zunfthaus am Neumarkt", "address": "Neumarkt 5, 8001 Zürich"}
{"entry_id": "889Q66TsV6pHS3wAdpXWZA", "businessname": "Landhus", "address": "Katzenbachstrasse 10, 8052 Zürich"}
{"entry_id": "4Gcr-wm8br_EG92qkZ2ZlQ", "businessname": "Store Sihlcity", "address": "Kalanderplatz 1, 8045 Zürich"}
{"entry_id": "KPXMYH5LZSgihdo1UZ6fuQ", "businessname": "Phuket Asia Center", "address": "Schöneggstrasse 21, 8004 Zürich"}
{"entry_id": "xQ5piiQ5peeZxbDQxwQk7Q", "businessname": "EquiTable AG", "address": "Stauffacherstrasse 163, 8004 Zürich"}
{"entry_id": "9OIo061XvdH0r4LmXxxqyw", "businessname": "Khujug", "address": "Schöneggstrasse 5, 8004 Zürich"}
{"entry_id": "pSNHIhKQobfCpYbRHGXpJA", "businessname": "Maison 33 Cafe & Bistro", "address": "Höschgasse 33, 8008 Zürich"}
{"entry_id": "CzZHlRmbQ0Ck5-K8jovoIA", "businessname": "Raclette-Stube", "address": "Zähringerstrasse 16, 8001 Zürich"}
{"entry_id": "HGl8JOiGkE_U6P81GHsQww", "businessname": "Wirtschaft Unterdorf", "address": "Katzenseestrasse 15, 8046 Zürich"}
{"entry_id": "ee5i63KsuwHVTYsxZkF0ug", "businessname": "Bodega Española", "address": "Münstergasse 15, 8001 Zürich"}
{"entry_id": "DFaH8FzqVGpXbnu1OIJKTw", "businessname": "Kaffeehandel", "address": "Münstergasse 19, 8001 Zürich"}
{"entry_id": "v5vK1szqlL_o7RrAlCnjzg", "businessname": "Tšüri Grill", "address": "Hönggerstrasse 13, 8037 Zürich"}
{"entry_id": "sJ5W3ik7dxJxaQlMSweSJQ", "businessname": "Restaurant HONGXI", "address": "Zwinglistrasse 3, 8004 Zürich"}
{"entry_id": "VGIurioVsxUO5E8IegyXfw", "businessname": "Zunfthaus zur Saffran", "address": "Limmatquai 54, 8001 Zürich"}
{"entry_id": "EJaiwjqTHKMPif4QKNqR5A", "businessname": "4 Tiere Bar", "address": "Feldstrasse 61, 8004 Zürich"}
{"entry_id": "oAOK4w6rY4CGltD4oNCeVQ", "businessname": "b.good International", "address": "Oberdorfstrasse 8, 8001 Zürich"}
{"entry_id": "32pNx0Nf6X1sTTgd2vAuEw", "businessname": "Acasa Suites Zürich", "address": "Binzmühlestrasse 72, 8050 Zürich"}
{"entry_id": "pohmXOz8DhG5nHneusttNg", "businessname": "Pizza Nation", "address": "Rosengasse 3, 8001 Zürich"}
{"entry_id": "fwz-yFxIGYMxCDLkue7_0g", "businessname": "Ristorante Amalfi", "address": "Mainaustrasse 23, 8008 Zürich"}
{"entry_id": "SLTAJZ8tymFJ7MGGpxus1g", "businessname": "Aubrey", "address": "Schiffbaustrasse 10, 8005 Zürich"}
{"entry_id": "FvSOfUv_8a1Qm5S1J44KtQ", "businessname": "Noerd Kantine", "address": "Binzmühlestrasse 170, 8050 Zürich"}
{"entry_id": "PQcEs0yix_K3zWtk40Kmkg", "businessname": "DORY & DU", "address": "Limmatpromenade 27, 5400 Baden"}
ENTRIES

printf '\nregistered: %d  failed: %d\n' "$ok" "$failed"
if [ "$failed" -gt 0 ]; then
  printf 'failed entries:\n' >&2
  printf '  %s\n' "${failures[@]}" >&2
  exit 1
fi
