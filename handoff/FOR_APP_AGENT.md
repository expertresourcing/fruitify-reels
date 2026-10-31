# Requests from the marketing assistant to the FRUiTIFY app agent

How this works (agreed with Ankur, 31 Oct 2026):
- The marketing assistant writes requests here. It only READS the app code and never changes it.
- The app agent reads this file at the start of each session, does what Ankur has approved, and writes its answer under "Reply from app agent" with the date.
- Status values: NEW -> APPROVED BY ANKUR -> DONE / NOT POSSIBLE (with reason).
- Nothing here is approved until Ankur marks it "APPROVED BY ANKUR" (or tells the app agent directly).

---

## R1 - Khalid General Store (Kanpur): check grocery items exist  | Status: NEW (31 Oct)
Shop: Khalid General Store, ID khalidgeneralstore, owner Mohammad Khalid, mobile 6393557026. Onboarded 31 Oct.
On WhatsApp (30 Oct) he sent a handwritten list plus pack photos of the items he wants to sell first:
| Item | Pack | MRP | His rate |
|---|---|---|---|
| Surf Excel (Easy Wash) detergent powder | 500 g | 74 | 70 |
| More Light (Extra Power) detergent powder | 500 g | 42 | 40 |
| More Light (Extra Power) detergent powder | 1 kg | 84 | 80 |
Please:
1. Check that these three products and pack sizes are in the ready grocery list (~130 items). Add any missing product or pack size to the list (name, brand, size; no internet brand photos - "Photo coming soon" until the shop uploads its own photo).
2. Reply here with: found / added, and the exact screen path a shop uses to add a grocery item (menu names and button names as they appear), so the marketing assistant can give Khalid correct click-by-click steps.
3. Optional, only if Ankur approves: add these 3 items to Khalid's shop for him so his shop is not empty on day one.
4. Does the app let a shop owner change the PIN after first login? If yes, give the path - his PIN is easy to guess and was shared on WhatsApp.

## R2 - Word rule on the /grow form  | Status: PARKED by Ankur (30 Oct, "we will change it later")
The short form shows "फल" in the intro line and on the first choice. Our vendor-facing word rule: write "Fruits", never फल / फलों / जोड़ें / जुड़ / कदम. Suggested: "Fruits, सब्ज़ी या किराना की दुकान है?" and choice "Fruits".

---
## Reply from app agent
(write below, newest first, with date)
