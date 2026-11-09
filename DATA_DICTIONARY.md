# Final data dictionary
Generated from final table schemas. Empty strings in source CSVs remain unknown/missing. Dates use ISO format. Report rows preserve amendments and do not represent uniquely deduplicated economic events.

## analytical transaction
| Field | Meaning | Missing/empty rows |
|---|---|---:|
| `transaction_id` | Chamber-prefixed source report/item identifier | 0 |
| `chamber` | House or Senate | 0 |
| `filing_id` | Original report identifier | 0 |
| `row_number` | Report item number | 0 |
| `politician` | Disclosure filer display name | 0 |
| `filing_date` | Report filing date when available | 6394 |
| `transaction_date` | Reported transaction date | 0 |
| `owner` | Reported household ownership | 3224 |
| `ticker` | Normalized reported ticker, not a permanent security ID | 0 |
| `asset_name` | Reported asset description | 0 |
| `asset_type` | Source asset classification | 0 |
| `transaction_type` | Source purchase/sale/exchange classification | 0 |
| `amount_raw` | Original disclosed amount bracket | 0 |
| `amount_min` | Lower bound, not an exact value | 6 |
| `amount_max` | Upper bound, may be missing/open-ended | 6 |
| `source_url` | Original disclosure link | 0 |
| `source_format` | PDF or archived HTML | 0 |
| `comment` | Source comment | 6276 |
| `review_flag` | Inherited extraction review flag | 518 |
| `ticker_status` | Ticker-resolution status | 518 |
| `month` | Transaction calendar month, YYYY-MM | 0 |
| `exclusion_reason` | Scope exclusion reason, empty for included rows | 6912 |
| `action` | Harmonized transaction category | 0 |

## ticker-month join
| Field | Meaning | Missing/empty rows |
|---|---|---:|
| `ticker` | Normalized reported ticker, not a permanent security ID | 0 |
| `month` | Transaction calendar month, YYYY-MM | 0 |
| `house_reports` | Per-chamber aggregate: house reports. Missing means no observation in that chamber, not observed zero. | 190 |
| `house_filings` | Per-chamber aggregate: house filings. Missing means no observation in that chamber, not observed zero. | 190 |
| `house_filers` | Per-chamber aggregate: house filers. Missing means no observation in that chamber, not observed zero. | 190 |
| `house_purchases` | Per-chamber aggregate: house purchases. Missing means no observation in that chamber, not observed zero. | 190 |
| `house_sales` | Per-chamber aggregate: house sales. Missing means no observation in that chamber, not observed zero. | 190 |
| `senate_reports` | Per-chamber aggregate: senate reports. Missing means no observation in that chamber, not observed zero. | 3410 |
| `senate_filings` | Per-chamber aggregate: senate filings. Missing means no observation in that chamber, not observed zero. | 3410 |
| `senate_filers` | Per-chamber aggregate: senate filers. Missing means no observation in that chamber, not observed zero. | 3410 |
| `senate_purchases` | Per-chamber aggregate: senate purchases. Missing means no observation in that chamber, not observed zero. | 3410 |
| `senate_sales` | Per-chamber aggregate: senate sales. Missing means no observation in that chamber, not observed zero. | 3410 |
| `_merge` | Join provenance: both, left_only, right_only | 0 |

## portfolio completion
| Field | Meaning | Missing/empty rows |
|---|---|---:|
| `chamber` | House or Senate | 0 |
| `filing_id` | Original report identifier | 0 |
| `politician` | Disclosure filer display name | 0 |
| `transaction_date` | Reported transaction date | 0 |
| `owner` | Reported household ownership | 13532 |
| `ticker` | Normalized reported ticker, not a permanent security ID | 4702 |
| `asset` | Reported asset description | 0 |
| `type` | Source purchase/sale/exchange classification | 0 |
| `amount` | Original disclosed amount bracket | 98 |
| `review` | Source-specific review/verification label; not a calibrated probability | 25931 |
| `source_url` | Original disclosure link | 0 |
| `date_quality` | Source date anomaly flag, not a corrected date | 31658 |