# EVB-IT Compliance (Sub-Part von ai-literacy-research)

**EVB-IT** = *Ergänzende Vertragsbedingungen für die Beschaffung von IT-Leistungen*,
herausgegeben vom **BMDS** (Bundesministerium für Digitales und Staatsmodernisierung,
evb-it.gov.de). Standardisierte Vertragsmuster für die **IT-Beschaffung der
öffentlichen Hand** (Kommunen, Schulen, Unis, Behörden, Bund/Land).

**Warum Sub-Part von ai-literacy:** KI-Kompetenz-Training (KKT) und Contextual
Intelligence verkaufen an genau diese Zielgruppen. EVB-IT + **EU AI Act** ist die
Compliance-Schnittstelle, die unser Art.-4-Content bedient — der Checker macht sie
operationalisierbar (später z.B. als „EVB-IT Readiness"-Lead-Magnet auf KKT).

## Wiederverwendete Quelle (GH)
Vendored Snapshot von **`aivot-digital/evb-it`** unter `vendor/evb-it/`
(MIT für Template/Doku + **CC-BY-4.0** für die BMDS-Vertragstexte; Logo ausgenommen).
Enthält maschinenlesbare EVB-IT-Verträge in Typst: `cloud`, `pflege-s`,
`ueberlassung-typ-b`. Attribution via `vendor/evb-it/NOTICE.md` + `LICENSE.md`.
Siehe auch `VergabeLab/vergabelab-community` (offene KI-Bausteine fürs Vergabewesen,
sekundär).

## Tool: `tools/evb_it_compliance_checker.py`
Deterministischer, abhängigkeitsarmer Checker (stdlib + pyyaml, JSON I/O).
Wissensbasis als Daten: `config/compliance/evb_it.yaml`.

**Ablauf:** `Profil` → passende **EVB-IT-Familien** (via `applies_when`-Prädikate)
→ **Pflichten** (mit `check` bedingt) → Status `ok`/`gap` (via `control`-Flag)
→ **Readiness-Score** (gewichtet nach Severity) + Empfehlungen.

**Prädikat-DSL** (sicher evaluiert, kein `eval`):
`{field, op, value}` mit `op ∈ {==,!=,in,not_in,>,<,>=,<=}`, kombiniert via
`{all:[…]}`, `{any:[…]}`, `{not:…}`.

### Profil-Schema (JSON-Eingabe)
- **Deskriptiv (Szenario):** `buyer_is_public_sector`, `buyer_type`, `service_type`
  (`cloud_saas|cloud_iaas|cloud_paas|software_dev|training_delivery|hardware_kauf|
  oss_transfer|project|framework|maintenance|ueberlassung`), `involves_personal_data`,
  `special_category_data`, `uses_ai`, `ai_high_risk`, `open_source_components`,
  `sovereignty_required`.
- **Kontrollen (was erfüllt ist / zu prüfen):** `dsgvo_av_contract_in_place`,
  `dsgvo_special_ok`, `subcontracting_approved`, `acceptance_procedure_defined`,
  `confidentiality_agreed`, `security_toms_defined`, `audit_rights_granted`,
  `liability_insurance_in_place`, `sovereignty_measured`, `ai_act_conformity_declared`,
  `oss_license_compliant`, `tender_compliant`.

### Aufruf
```bash
python tools/evb_it_compliance_checker.py --profile profile.json \
  [--kb config/compliance/evb_it.yaml] [--json out.json] [--markdown out.md]
```

### Beispiel-Report (Kommune kauft KI-Literacy-Training für Schulen via SaaS)
- Anwendbare Familien: `general` + `cloud`
- 13 Pflichten, 9 Lücken, **5 kritisch** → Readiness **21.4 % — nicht bereit**
- U.a. Lücken: DSGVO-AV-Vertrag, DSGVO bes. Kat. (Schüler), EU AI Act (High-Risk),
  Digitale Souveränität, EVB-IT Cloud §Unterauftragnehmer, §Sicherheit/TOM, §Prüfrechte
- Cloud-Pflichten sind direkt auf `vendor/evb-it/evb-it/cloud/cloud-vertrag.typ`
  (Zeilennachweise, z.B. §Datenschutz Z.775) zurückgeführt.

## Coverage-Hinweis
Vollständig aus dem vendored Repo extrahiert: **Cloud, Pflege S, Überlassung Typ B**.
Weitere Familien (Dienstleistung, Kauf, Transfer, PB, System, Rahmenvereinbarung)
sind aus den BMDS-EVB-IT-Grundsätzen recherchiert und als `bmds_research` markiert
(nicht im vendored Repo enthalten) — bei Repo-Erweiterung nachpflegen.

## Lizenz / Attribution (wichtig)
- BMDS-Vertragstexte: **CC-BY-4.0** — Bei Nutzung/Weitergabe Namensnennung BMDS
  (`DSII2@bmds.bund.de`) erforderlich (siehe `vendor/evb-it/NOTICE.md`).
- Repo-eigene Bestandteile (Template, Doku): **MIT**.
- **EVB-IT-Logo nicht** weiterverwenden.
- **Keine Rechtsberatung:** verbindlich sind die amtlichen Vertragstexte in aktueller Fassung.

## Tests
`tests/unit/test_evb_it_checker.py` (pytest): Familien-Applikabilität, Grounding der
Cloud-Pflichten im vendored Repo, OSS-Familie, Readiness-Logik, voll-erfülltes Profil,
DSL-Robustheit bei leerem Profil.
