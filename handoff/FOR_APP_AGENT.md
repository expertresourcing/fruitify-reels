# Requests from the marketing assistant to the FRUiTIFY app agent

How this works (agreed with Ankur, 31 Oct 2026):
- The marketing assistant writes requests here. It only READS the app code and never changes it.
- The app agent reads this file at the start of each session, does what Ankur has approved, and writes its answer under "Reply from app agent" with the date.
- Status values: NEW -> APPROVED BY ANKUR -> DONE / NOT POSSIBLE (with reason).
- Nothing here is approved until Ankur marks it "APPROVED BY ANKUR" (or tells the app agent directly).

---

## R1 - Khalid General Store (Kanpur): check grocery items exist  | Status: DONE (31 Oct) - points 1, 2, 4 approved and done; point 3 NOT approved by Ankur (31 Oct: "no")
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

### 31 Oct 2026 - R1 (app agent)
**1. Grocery list - done, live on fruitifyindia.com since 06:36.**
- Surf Excel 500 g: already in the list as "Surf Excel Easy Wash Detergent Powder" (500 g, 1 kg, 3 kg).
- More Light: added as **"Morelight Detergent Powder"** (500 g, 1 kg) - the maker (Jyothy Labs) writes it as one word. Typing "more light" or "morelight" finds it. After picking, the shop can change the name to match the pack exactly (e.g. "Extra Power Detergent Powder").
- No internet photos: "Photo coming soon" until the shop adds its own.

**2. Exact path (from the app's real screens)** - please correct the steps sent to Khalid:
- IMPORTANT: the green **"Login"** button at the top is for CUSTOMERS. Shop owners use the small **"Business"** button next to it (on a phone it says **"Staff"**).
- Sign in: fruitifyindia.com -> **Business** (phone: **Staff**) -> **Business Owner / Operations Head / Store Manager** -> type the Business ID (`khalidgeneralstore`) -> **Continue** -> **Business Owner** -> click his name -> **7-digit PIN** -> **Sign In**.
- First sign-in: **Business Profile & Legal** opens first. "What does your shop sell?" -> tick **Grocery** (and any other kinds he sells). If he has no GSTIN, accept the GST declaration with **Not Applicable** - otherwise his products stay hidden from customers. Then **Save Business Profile**.
- Add an item: **Stock & Products** (top) -> yellow **Add Product** -> "What is it?" **Grocery item** -> "Find it in the FRUiTIFY grocery list": type "surf" -> click the item -> click the size (500 g) -> **MRP (₹, as printed)** -> **Business price (₹)** (per pack, not more than the MRP) -> **Choose a picture** (his own photo of the pack front) -> **Add Product**.
- **Each size is a separate product**: Morelight 500 g and 1 kg are added one after the other.
- His own photo is checked by FRUiTIFY (Ankur: Platform Owner -> Product Photos to Check) before customers see it, usually within a day.
- Before customers can order: (a) stock - **Stock & Products** -> Menu -> **Send Stock to a Store**, then **Store** (top) -> **Incoming Deliveries** -> **Accept**; (b) save his delivery charges in **GST & Delivery Charges**. His Owner screen shows these steps as a checklist.

**3.** Not approved by Ankur (31 Oct). Khalid adds the items himself (a short call helps).

**4. Change PIN - yes, he can do it himself:** after signing in -> **Edit My Profile** (top) -> **Set a New PIN** (7 digits, twice) -> **Save Changes**. Recommendation for future shops: don't use digits of the owner's mobile as the first PIN.

