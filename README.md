# Nexiv.AI • Autonomous Institutional Financial Intelligence

**Nexiv.AI** is a cloud-native, institutional-grade financial intelligence engine specializing in **Indian Equities (NSE/BSE)**, **Live Indian IPOs (with Grey Market Premium / GMP)**, and **Global Stocks (US/Global)**.

Built on **5,053 pages of codified quantitative literature** from 7 financial legends:
* **Aswath Damodaran** (Discounted Cash Flow & Country Equity Risk Premiums)
* **McKinsey & Co.** (Key Value Driver, ROIC vs WACC Value Spread)
* **Benjamin Graham & David Dodd** (Margin of Safety & Net-Net Liquidation Floors)
* **Richard Brealey & Stewart Myers** (Capital Structure & Hurdle Rates)
* **Marcos López de Prado** (Triple Barrier Methods & Bet Sizing)
* **Howard Marks** (Credit & Market Cycle Positioning)
* **Howard M. Schilit** (Financial Shenanigans & Forensic Accounting)

---

## ⚡ 1-Click Cloud Deployment to Vercel (24/7 Mobile Access Without Mac)

Because **Nexiv.AI** has all 5,053 pages of knowledge and datasets bundled directly inside `nexiv_brain/`, it requires **zero external files or local Mac servers**. You can deploy it to Vercel in 60 seconds and access it permanently from your phone.

### Option A: Via GitHub (Recommended)
1. Initialize git and commit:
   ```bash
   git add .
   git commit -m "Deploy Nexiv.AI to Vercel"
   ```
2. Push this folder to a GitHub repository (e.g. `github.com/your-username/nexiv-ai`).
3. Log in to [vercel.com](https://vercel.com) and click **"Add New Project"**.
4. Import your `nexiv-ai` repository and click **Deploy**.
5. Done! Vercel will give you a permanent HTTPS URL like `https://nexiv-ai.vercel.app` that works on your phone anytime, anywhere in India and globally!

### Option B: Via Vercel CLI (Instant)
Run in this directory:
```bash
npx vercel
```
Follow the 3 prompts (hit Enter to accept defaults), and your live mobile URL is active!

---

## 🚀 Local Run (Development)

To run locally on your Mac or local network:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 cbm_server.py
```
Open on Mac: `http://localhost:8000`  
Open on Phone: `http://<your-mac-ip>:8000`

---

## 📱 Features

1. **Indian Stock Engine**:
   * Smart resolver for NSE & BSE (`RELIANCE`, `TCS`, `TATAMOTORS`, `ZOMATO`, `HDFCBANK`, etc.).
   * Formatted in Indian Rupees (₹) with tailored Indian cost of capital and 10Y G-Sec bond yields.
2. **Live Indian IPO & GMP Tracker**:
   * Tracks active/upcoming Indian IPOs (Mainboard & SME).
   * Displays Issue Price Band (₹), Lot Size, Minimum Retail Investment, and Live Grey Market Premium (GMP).
   * Unambiguous decisions: `APPLY FOR LONG TERM COMPOUNDER`, `APPLY FOR LISTING GAINS ONLY`, `AVOID / DO NOT APPLY`.
3. **Forensic Safety Shield**:
   * Altman Z-Score (Insolvency Risk)
   * Beneish M-Score (Earnings Manipulation)
   * Piotroski F-Score (Fundamental Momentum /9)
   * Sloan Cash Accruals (Quality of Cash Flow)
4. **Autonomous 4-Agent Council**:
   * Valuation Agent, Forensics Agent, Risk & Sizing Agent, Market Cycle Agent.
