"""
Codified Knowledge Repository and Cognitive Modules for Nexiv.AI.
Contains:
1. The 15 Top Financial Academic & Research Institutions (Harvard, Stanford, MIT, Oxford, Chicago, Wharton, Cambridge, LSE, UC Berkeley, NUS, NYU Stern, Columbia, Yale, LBS, Imperial College)
2. The 15 Top Financial Titans / Minds organized into 5 Categories (Buffett, Marks, Lynch, Smith, Dalio, Druckenmiller, El-Erian, Jones, Damodaran, Asness, Fink, Dimon, Griffin, Tepper, Housel)
3. Real-World Macroeconomic & World Market Situation Briefings (Sep-Oct 2026)
4. Advanced Gibberish / Keyboard Mashing Detection
5. Emotional Intelligence & Psychological Counseling Engine
6. Multi-Disciplinary Mental Models & Life Finance Frameworks
"""

import re
from typing import Dict, Any, List, Optional

class NexivCouncilKnowledge:
    """Institutional Knowledge Vault and Multi-Talented Cognitive Frameworks."""

    # =========================================================================
    # 1. THE 15 TOP GLOBAL ACADEMIC & RESEARCH INSTITUTIONS IN FINANCE
    # =========================================================================
    TOP_15_INSTITUTIONS = {
        "harvard": {
            "name": "Harvard University",
            "school": "Harvard Business School (HBS) & Department of Economics",
            "nobel_laureates_and_pioneers": "Michael Porter, John Lintner, Robert Merton, Kenneth Rogoff, Larry Summers",
            "seminal_breakthroughs": [
                "Porter's Five Forces Framework: Quantifying industry attractiveness and structural economic moats.",
                "Lintner's CAPM & Corporate Dividend Policy: Pioneered capital asset pricing and dividend stickiness research.",
                "Case Study Method in Corporate Finance: Codified empirical corporate restructuring, M&A valuation, and LBO modeling.",
                "Intergenerational Endowment Compounding: Institutional frameworks for long-term multi-generational capital stewardship."
            ],
            "core_doctrine": "Competitive strategy, sustainable structural moats, and corporate capital budgeting under competitive pressure.",
            "rule_in_nexiv": "A company without a structural competitive moat (Porter's Five Forces) will inevitably see its excess returns competed away to zero."
        },
        "stanford": {
            "name": "Stanford University",
            "school": "Stanford Graduate School of Business (GSB)",
            "nobel_laureates_and_pioneers": "William F. Sharpe, Myron Scholes, Kenneth Arrow, Paul Milgrom, Robert Wilson",
            "seminal_breakthroughs": [
                "The Sharpe Ratio (William Sharpe): The global benchmark formula measuring risk-adjusted excess returns ($S = (R_p - R_f) / \sigma_p$).",
                "Capital Asset Pricing Model (CAPM): Isolating systematic market risk ($\beta$) from diversifiable idiosyncratic risk.",
                "Venture Capital & Staged Financing Economics: The canonical mathematics of equity dilution, term sheets, and unicorn valuation.",
                "Auction Theory & Market Microstructure: Designing efficient electronic capital auctions and price discovery mechanisms."
            ],
            "core_doctrine": "Risk-adjusted performance optimization, quantitative beta decoupling, and innovation asset underwriting.",
            "rule_in_nexiv": "Never evaluate raw return without dividing by volatility; high returns achieved through reckless volatility destroy capital over time."
        },
        "mit": {
            "name": "Massachusetts Institute of Technology (MIT)",
            "school": "MIT Sloan School of Management & Department of Economics",
            "nobel_laureates_and_pioneers": "Fischer Black, Robert C. Merton, Paul Samuelson, Franco Modigliani, Andrew Lo, Stewart Myers",
            "seminal_breakthroughs": [
                "Continuous-Time Finance & Option Pricing: Formulated the mathematics that birthed the multi-trillion dollar derivatives industry.",
                "The Merton Credit Default Model: Modeling corporate equity as a call option on firm assets to calculate default probability.",
                "Pecking Order Theory (Stewart Myers): Proven corporate financing hierarchy: Internal retained cash first, safe debt second, external equity dilution last.",
                "The Adaptive Markets Hypothesis (Andrew Lo): Reconciling market efficiency with behavioral human psychological biases."
            ],
            "core_doctrine": "Mathematical rigor, continuous-time stochastic pricing, dynamic hedging, and capital structure optimization.",
            "rule_in_nexiv": "Treat equity as a residual claim; when corporate debt exceeds sustainable asset floors, equity holders face total wipeout."
        },
        "oxford": {
            "name": "University of Oxford",
            "school": "Saïd Business School & Department of Economics",
            "nobel_laureates_and_pioneers": "John Hicks, James Meade, Amartya Sen, Colin Mayer, Ludovic Phalippou",
            "seminal_breakthroughs": [
                "Oxford Private Equity & Infrastructure Finance Frameworks: Empirical benchmarking of PE fee structures and real returns.",
                "Mega-Project Infrastructure Discounting: Long-horizon valuation frameworks for energy, rail, and civil infrastructure assets.",
                "Corporate Purpose & Stakeholder Governance: Research proving firms with long-term stakeholder alignment exhibit lower credit default spreads.",
                "Stranded Asset Pricing: Early quantitative modeling of climate transition risks on fossil fuel balance sheets."
            ],
            "core_doctrine": "Long-horizon infrastructure capital allocation, corporate purpose governance, and real-asset valuation.",
            "rule_in_nexiv": "Discount multi-decade capital projects with explicit accounting for governance friction and asset obsolescence."
        },
        "chicago": {
            "name": "University of Chicago",
            "school": "Booth School of Business & Kenneth C. Griffin Department of Economics",
            "nobel_laureates_and_pioneers": "Eugene Fama, Harry Markowitz, Merton Miller, Milton Friedman, Richard Thaler, Lars Peter Hansen",
            "seminal_breakthroughs": [
                "The Efficient Market Hypothesis (Eugene Fama): Proof that market prices rapidly reflect known information.",
                "Modern Portfolio Theory (Harry Markowitz): Mathematical Mean-Variance Optimization and the Efficient Frontier.",
                "The Fama-French Multi-Factor Models: Proving systematic market alpha stems from Size (SMB), Value (HML), Profitability, and Investment factors.",
                "Modigliani-Miller Theorems (Merton Miller): Capital structure and dividend irrelevance in frictionless markets.",
                "Behavioral Economics & Mental Accounting (Richard Thaler): Human biases (endowment effect, loss aversion) that create persistent market anomalies."
            ],
            "core_doctrine": "The intellectual home of empirical asset pricing, systematic factor premiums, and market efficiency vs behavioral friction.",
            "rule_in_nexiv": "Do not attempt to outguess liquid market pricing on short-term noise; capture systematic risk factor premiums over multi-year cycles."
        },
        "upenn": {
            "name": "University of Pennsylvania",
            "school": "The Wharton School",
            "nobel_laureates_and_pioneers": "Jeremy Siegel, Marshall Blume, Joseph Wharton, Simon Kuznets, Lawrence Klein",
            "seminal_breakthroughs": [
                "Stocks for the Long Run (Jeremy Siegel): 200+ years of definitive empirical data proving equities compound at ~6.5%-7.0% real annualized return, beating all other asset classes.",
                "Blume Beta Adjustment: Statistical proof that company betas mean-revert toward 1.0 over time.",
                "Wharton Pension & Retirement Wealth Management: Asset-Liability Matching (ALM) models and longevity risk preservation.",
                "Real Estate Investment Trust (REIT) Valuation: Capitalization rate modeling and commercial property cash flow underwriting."
            ],
            "core_doctrine": "Empirical long-run equity compounding, institutional wealth management, and real-world asset allocation.",
            "rule_in_nexiv": "Equities are the single most reliable long-term engine of real purchasing power, provided you never panic-sell during cyclical downturns."
        },
        "cambridge": {
            "name": "University of Cambridge",
            "school": "Judge Business School & Faculty of Economics",
            "nobel_laureates_and_pioneers": "John Maynard Keynes, Alfred Marshall, Arthur Pigou, Richard Stone, Angus Deaton",
            "seminal_breakthroughs": [
                "Keynesian Macroeconomics & Liquidity Preference Theory: Explaining liquidity traps, speculative money demand, and animal spirits.",
                "Cambridge Centre for Alternative Finance (CCAF): The world's leading academic benchmark on Global Fintech, Crypto-Assets, and RegTech.",
                "Catastrophe & Macro-Systemic Risk Modeling (Cambridge Risk Studies): Quantifying black swan scenarios on global asset classes.",
                "Keynes' Discretionary Value Portfolio: Managing the King's College Chest, pioneering bottom-up value investing before Wall Street adopted it."
            ],
            "core_doctrine": "Macroeconomic liquidity cycles, institutional crisis resilience, and alternative fintech financial architecture.",
            "rule_in_nexiv": "Markets can remain irrational longer than you can remain solvent; always maintain surplus liquidity to survive unpredictable liquidity crunches."
        },
        "lse": {
            "name": "London School of Economics (LSE)",
            "school": "Department of Finance & Systemic Risk Centre (SRC)",
            "nobel_laureates_and_pioneers": "Charles Goodhart, Christopher Pissarides, Friedrich Hayek, Ronald Coase, Amartya Sen",
            "seminal_breakthroughs": [
                "Systemic Risk Centre (SRC): World-leading research on financial network contagion, domino insolvencies, and liquidity evaporation.",
                "Goodhart's Law (Charles Goodhart): 'When a measure becomes a target, it ceases to be a good measure' (crucial for financial metrics and central banking).",
                "Financial Markets Group (FMG): Advanced research on cross-border capital flows, sovereign bond spreads, and banking regulation.",
                "The Nature of the Firm (Ronald Coase): Transaction cost economics determining why corporations exist and how they organize capital."
            ],
            "core_doctrine": "Systemic risk transmission, endogenous market liquidity, and institutional regulatory economics.",
            "rule_in_nexiv": "Liquidity is a coward: it disappears the moment you need it most. Never rely on market liquidity to exit an oversized position in a panic."
        },
        "berkeley": {
            "name": "University of California, Berkeley",
            "school": "Haas School of Business & Department of Economics",
            "nobel_laureates_and_pioneers": "Mark Rubinstein, George Akerlof, Daniel Kahneman, Hal Varian, David Romer",
            "seminal_breakthroughs": [
                "The Cox-Ross-Rubinstein (CRR) Binomial Options Model: The foundational discrete-time lattice for pricing complex options and American derivatives.",
                "The Market for Lemons & Information Asymmetry (George Akerlof): Proving adverse selection collapses markets where seller information is opaque.",
                "Prospect Theory & Loss Aversion (Daniel Kahneman at Berkeley): The mathematical proof that financial losses cause 2.5x more psychological pain than equal gains.",
                "Network Economics & Platform Economics (Hal Varian): Valuation laws for digital software, zero-marginal-cost goods, and tech platforms."
            ],
            "core_doctrine": "Information asymmetry economics, behavioral prospect theory, and non-linear options pricing lattices.",
            "rule_in_nexiv": "Information asymmetry destroys uninformed capital; if you do not understand the seller's motivation (e.g. high-OFS IPOs), you are the mark."
        },
        "nus": {
            "name": "National University of Singapore (NUS)",
            "school": "NUS Business School & Risk Management Institute (RMI)",
            "nobel_laureates_and_pioneers": "Duan Jin-Chuan, Joseph Cherian, Lim Kian Guan",
            "seminal_breakthroughs": [
                "Credit Research Initiative (CRI): Non-parametric global corporate Default Probabilities (PD) covering 80,000+ public companies across 130 economies.",
                "Asian Capital Markets & Conglomerate Finance: The premier global authority on Asian corporate governance, family-controlled conglomerates, and state-backed enterprises.",
                "Sovereign Wealth Management Economics: The operational study of Temasek and GIC's multi-decade generational wealth preservation.",
                "Fintech & Digital Banking Architecture: Regulatory sandbox design and cross-border instant settlement networks in emerging Asia."
            ],
            "core_doctrine": "Global corporate credit default modeling, Asian emerging market corporate finance, and sovereign wealth compounding.",
            "rule_in_nexiv": "Continuous corporate default probability monitoring is essential; balance sheet deterioration gives measurable quantitative signals months before credit ratings downgrade."
        },
        "nyu": {
            "name": "New York University (NYU)",
            "school": "Leonard N. Stern School of Business",
            "nobel_laureates_and_pioneers": "Aswath Damodaran, Edward Altman, Robert Engle, Nouriel Roubini, Roy Smith",
            "seminal_breakthroughs": [
                "The Altman Z-Score (Edward Altman): The global gold standard predictive formula for corporate insolvency and bankruptcy risk.",
                "Comprehensive Corporate Valuation & DCF Frameworks (Aswath Damodaran): The worldwide open-source benchmark for Equity Risk Premiums, Cost of Capital, and FCFF valuation.",
                "ARCH / GARCH Volatility Modeling (Robert Engle - Nobel Laureate): Mathematical time-series modeling of financial asset volatility clustering.",
                "Macroeconomic Debt Bubbles & Crisis Forecasting (Nouriel Roubini): Early quantitative detection of sovereign and real estate credit crises."
            ],
            "core_doctrine": "Intrinsic cash flow valuation, credit insolvency diagnostics, and econometric volatility clustering.",
            "rule_in_nexiv": "Cash flow is undeniable reality, accounting earnings are an opinion; never buy a company without computing its Damodaran DCF and Altman Z-Score."
        },
        "columbia": {
            "name": "Columbia University",
            "school": "Columbia Business School (CBS) & Department of Economics",
            "nobel_laureates_and_pioneers": "Benjamin Graham, David Dodd, Joseph Stiglitz, Joel Greenblatt, Bruce Greenwald",
            "seminal_breakthroughs": [
                "The Birthplace of Value Investing (1934): Benjamin Graham and David Dodd published 'Security Analysis', creating the entire discipline of fundamental securities research.",
                "Margin of Safety & Net-Net Working Capital: The immutable requirement of buying assets at a verifiable discount to conservative liquidation value.",
                "Earning Power Value (EPV) (Bruce Greenwald): Valuing operating earnings without speculative growth projections.",
                "The Magic Formula of Value Investing (Joel Greenblatt): Screening for companies combining high Return on Capital with high Earnings Yield.",
                "Information Asymmetry & Credit Rationing (Joseph Stiglitz - Nobel Laureate): Why banks ration credit rather than raising interest rates."
            ],
            "core_doctrine": "The ancestral home of fundamental value investing, Margin of Safety, and balance sheet liquidation floors.",
            "rule_in_nexiv": "The function of the Margin of Safety is to render unnecessary an accurate estimate of the future."
        },
        "yale": {
            "name": "Yale University",
            "school": "Yale School of Management (SOM) & Department of Economics",
            "nobel_laureates_and_pioneers": "David F. Swensen, Robert J. Shiller, Irving Fisher, William Nordhaus, James Tobin",
            "seminal_breakthroughs": [
                "The Yale Endowment Model (David Swensen): Pioneering asset allocation shifting from liquid public equities into illiquid, high-alpha alternative assets (Venture, PE, Real Assets, Absolute Return).",
                "The Cyclically Adjusted Price-to-Earnings (CAPE) Ratio (Robert Shiller - Nobel Laureate): 10-year inflation-adjusted P/E ratio that accurately predicts 10-year forward equity returns.",
                "Behavioral Asset Bubbles & 'Irrational Exuberance' (Robert Shiller): Proving housing and stock market bubbles are driven by social contagion and narrative feedback loops.",
                "Tobin's Q Ratio (James Tobin - Nobel Laureate): Market value of a firm divided by the replacement cost of its tangible assets."
            ],
            "core_doctrine": "The illiquidity premium, institutional endowment asset allocation, and macro valuation mean-reversion.",
            "rule_in_nexiv": "When market-wide CAPE ratios reach historical extremes, future 10-year forward returns will be muted; adjust asset allocation accordingly."
        },
        "lbs": {
            "name": "London Business School (LBS)",
            "school": "Finance Subject Area",
            "nobel_laureates_and_pioneers": "Richard Brealey, Stewart Myers, Elroy Dimson, Paul Marsh, Mike Staunton",
            "seminal_breakthroughs": [
                "Principles of Corporate Finance (Richard Brealey & Stewart Myers): The global master textbook defining Net Present Value (NPV) and corporate capital structure.",
                "Triumph of the Optimists (Dimson, Marsh, Staunton): The definitive 120-year empirical database tracking long-run equity risk premiums across 23 global economies.",
                "Centre for Corporate Governance: Groundbreaking empirical research on executive compensation, board independence, and activist shareholder value creation.",
                "Private Equity & M&A Hurdle Rates: Precision models for corporate cost of capital and international diversification."
            ],
            "core_doctrine": "Global long-run capital returns, corporate capital structure, and empirical hurdle rate discipline.",
            "rule_in_nexiv": "An investment operation is only justifiable if its Net Present Value is positive when discounted at the true opportunity cost of capital."
        },
        "imperial": {
            "name": "Imperial College London",
            "school": "Imperial College Business School & Mathematical Finance Group",
            "nobel_laureates_and_pioneers": "Damiano Brigo, Rama Cont, Johannes Muhle-Karbe",
            "seminal_breakthroughs": [
                "Quantitative Financial Engineering & Stochastic Calculus: World-class models for jump-diffusion processes, interest rate term structure, and counterparty credit risk (CVA/DVA).",
                "Center for Financial Technology: Advanced algorithmic execution, high-frequency limit order book dynamics, and market microstructure simulation.",
                "Climate & Clean Energy Quantitative Finance: Mathematical pricing of carbon credit derivatives, renewable transition risks, and green bond premiums.",
                "Deep Learning & AI in Quantitative Asset Management: Neural network architectures for high-dimensional alpha signal extraction."
            ],
            "core_doctrine": "Stochastic quantitative modeling, high-frequency market microstructure, and computational algorithmic alpha.",
            "rule_in_nexiv": "Order execution and market microstructure friction consume significant alpha; quantitative execution algorithms must optimize entry timing and slippage."
        }
    }

    TOP_15_ACADEMIC_INSTITUTIONS = TOP_15_INSTITUTIONS

    # =========================================================================
    # 2. THE 15 TOP GLOBAL INVESTMENT FIRMS & ASSET ALLOCATORS
    # =========================================================================
    TOP_15_INVESTMENT_FIRMS = {
        "blackrock": {
            "name": "BlackRock",
            "leader": "Larry Fink",
            "aum": "$10.5+ Trillion",
            "core_philosophy": "Aladdin Risk Engine & Multi-Asset Factor Allocation",
            "doctrine": "World's largest asset manager. Pioneers of the Aladdin enterprise risk engine, modeling correlated risk across 100,000+ factors. Dominates low-cost passive index ETFs (iShares), factor investing (momentum, value, quality), and long-term capital transition into energy and digital infrastructure.",
            "rule": "Manage portfolio risk at the factor level, not just the stock ticker level. True diversification requires uncorrelated asset drivers."
        },
        "bridgewater": {
            "name": "Bridgewater Associates",
            "leader": "Ray Dalio",
            "aum": "$125+ Billion",
            "core_philosophy": "The Economic Machine & All-Weather Risk Parity",
            "doctrine": "The largest hedge fund in history. Built on Dalio's economic template: the economy is driven by transactions, the short-term debt cycle (5-8 years), and the long-term debt cycle (75-100 years). Created the All-Weather Strategy, allocating risk equally across 4 economic environments: rising growth, falling growth, rising inflation, and falling inflation.",
            "rule": "He who lives by the crystal ball will eat shattered glass. Balance your asset risks so no single economic environment can wipe you out."
        },
        "renaissance": {
            "name": "Renaissance Technologies / Rentec",
            "leader": "Jim Simons",
            "aum": "$50+ Billion (Medallion Fund)",
            "core_philosophy": "Mathematical Statistical Arbitrage & Algorithmic Objectivity",
            "doctrine": "The most profitable quantitative fund in history (averaging 66% gross annualized returns for 30+ years). Employs mathematicians, cryptographers, and physicists. Uses non-linear mathematical models to detect anomalous micro-patterns in market pricing that human intuition cannot see, trading with automated algorithmic discipline.",
            "rule": "Human emotions—fear, hope, and greed—distort prices. Mathematical models that eliminate human psychological bias are the purest edge in markets."
        },
        "citadel": {
            "name": "Citadel",
            "leader": "Ken Griffin",
            "aum": "$65+ Billion",
            "core_philosophy": "Multi-Strategy Pod Architecture & High-Frequency Risk Limits",
            "doctrine": "A premier alternative asset manager and global market maker. Operates independent, specialized investment 'pods' across equities, commodities, fixed income, and quantitative strategies. Strict risk limits enforce instantaneous risk reduction upon drawdowns, allowing capital to flow dynamically to where market mispricings are widest.",
            "rule": "Relentless risk underwriting, extreme execution precision, and never tolerating undisciplined downside drift."
        },
        "berkshire": {
            "name": "Berkshire Hathaway",
            "leader": "Warren Buffett & Charlie Munger",
            "aum": "$1.0+ Trillion Market Cap",
            "core_philosophy": "Permanent Capital, Durable Moats & Owner Earnings",
            "doctrine": "The pinnacle of value compounding. Invests in businesses with durable competitive advantages ('economic moats'), strong pricing power, high return on equity with little debt, and shareholder-oriented management. Capital is funded by insurance float, allowing permanent holding periods ('our favorite holding period is forever').",
            "rule": "It is far better to buy a wonderful company at a fair price than a fair company at a wonderful price."
        },
        "goldman": {
            "name": "Goldman Sachs",
            "leader": "David Solomon",
            "aum": "$2.8+ Trillion Assets Under Supervision",
            "core_philosophy": "Global Investment Research & Equity Capital Underwriting",
            "doctrine": "Wall Street's premier investment bank and research powerhouse. Dominates global M&A advisory, primary equity underwriting, and institutional market making. Tracks global macroeconomic thematic shifts, commodity super-cycles, and structural corporate earnings trends across global exchanges.",
            "rule": "Liquidity and capital structure drive corporate survival; always monitor institutional fund flows and debt maturities."
        },
        "morgan_stanley": {
            "name": "Morgan Stanley",
            "leader": "Ted Pick",
            "aum": "$3.1+ Trillion Wealth & Asset Management",
            "core_philosophy": "Counterpoint Global & Secular Tech Disruptor Investing",
            "doctrine": "Global financial services leader. Home to Counterpoint Global, focusing on companies with unique market positions benefiting from long-term, secular disruptive innovation. Emphasizes comprehensive asset allocation, private wealth preservation, and global thematic research.",
            "rule": "Look for secular disruptors with expansive Total Addressable Markets (TAM) rather than mere cyclical rebound plays."
        },
        "jpmorgan": {
            "name": "JPMorgan Chase",
            "leader": "Jamie Dimon",
            "aum": "$3.9+ Trillion Balance Sheet",
            "core_philosophy": "The Fortress Balance Sheet & Global Liquidity Stewardship",
            "doctrine": "The largest bank in the Western world. Built on Jamie Dimon's principle of the 'Fortress Balance Sheet'—holding excess Tier 1 common equity, deep liquidity reserves, and rigorous credit stress-testing to survive any economic hurricane while aggressively seizing distressed assets at the bottom of cycles.",
            "rule": "Hope is not a strategy. Run your finances so that you can survive the worst possible storm without government or third-party bailouts."
        },
        "mckinsey": {
            "name": "McKinsey & Company",
            "leader": "Tim Koller & Marc Goedhart",
            "aum": "Advisory on trillions in global corporate capital",
            "core_philosophy": "The Fundamental Law of Value Creation: ROIC > WACC",
            "doctrine": "Authors of the seminal treatise 'Valuation: Measuring and Managing the Value of Companies'. Proven law: Companies create shareholder value only when their Return on Invested Capital (ROIC) exceeds their Weighted Average Cost of Capital (WACC). Revenue growth without ROIC destroys corporate value.",
            "rule": "Accounting net income is an opinion; cash return on invested capital relative to cost of capital is mathematical reality."
        },
        "oaktree": {
            "name": "Oaktree Capital Management",
            "leader": "Howard Marks",
            "aum": "$190+ Billion",
            "core_philosophy": "Second-Level Thinking & Credit Asymmetry",
            "doctrine": "World leader in credit, high-yield bonds, and distressed debt. Guided by Howard Marks' iconic memos. Operates with asymmetric risk control: prioritizing the containment of loss over the pursuit of gain. Asserts that investor psychology swings like a pendulum between irrational euphoria and unwarranted panic.",
            "rule": "Rule No. 1: Most things prove to be cyclical. Rule No. 2: Some of the greatest opportunities come when other people forget Rule No. 1."
        },
        "two_sigma": {
            "name": "Two Sigma",
            "leader": "John Overdeck & David Siegel",
            "aum": "$60+ Billion",
            "core_philosophy": "Data Science, Alternative Datasets & Machine Learning Alpha",
            "doctrine": "Pioneered applying big data, machine learning, and high-performance computing to quantitative trading. Ingests petabytes of alternative data (satellite imagery, freight manifests, web scraping, weather patterns) to uncover predictive economic signals before traditional financial metrics report them.",
            "rule": "Financial markets are complex adaptive systems; use the rigorous scientific method to validate hypotheses rather than relying on gut feeling."
        },
        "millennium": {
            "name": "Millennium Management",
            "leader": "Israel Englander",
            "aum": "$68+ Billion",
            "core_philosophy": "Market-Neutral Pods & Strict Drawdown Halts",
            "doctrine": "One of the most consistently profitable multi-strategy hedge funds in history. Employs 300+ independent trading pods under strict risk boundaries. Pods that suffer a 5% drawdown have their capital cut by 50%; pods that reach a 7.5% drawdown are immediately shut down. Delivers smooth, non-correlated market-neutral returns.",
            "rule": "Preserve principal at all costs. Never give a losing trade room to wipe out months of hard-earned gains."
        },
        "elliott": {
            "name": "Elliott Management",
            "leader": "Paul Singer",
            "aum": "$65+ Billion",
            "core_philosophy": "Activist Governance & Unlocking Balance Sheet Traps",
            "doctrine": "The world's most formidable activist investment fund. Conducts relentless operational and legal due diligence to find undervalued companies with lazy or misaligned corporate boards. Unlocks hidden shareholder value by demanding spin-offs, board changes, dividend increases, and operational streamlining.",
            "rule": "Do not passively accept corporate underperformance; actively demand capital efficiency and governance integrity."
        },
        "tiger_global": {
            "name": "Tiger Global",
            "leader": "Chase Coleman",
            "aum": "$50+ Billion",
            "core_philosophy": "Secular Software Growth & TAM Scaling",
            "doctrine": "Founded by Julian Robertson's protégé Chase Coleman. Specializes in global internet, software, and fintech companies with massive Total Addressable Markets (TAM) and high operating leverage. Backs founders who build viral network effects and unit economics that scale exponentially.",
            "rule": "Bet heavily on generational technology shifts where winner-take-most dynamics compound over decades."
        },
        "temasek_gic": {
            "name": "Temasek / GIC",
            "leader": "Singapore Sovereign Wealth",
            "aum": "$700+ Billion Combined",
            "core_philosophy": "Multi-Decade Intergenerational Compounding",
            "doctrine": "The benchmark for sovereign wealth compounding globally. Invests with a 20-to-30 year generational horizon. Focuses on structural megatrends: Digitization, Sustainable Living, Future of Consumption, and Long Life/Healthcare. Provides patient, resilient anchor capital through global crises.",
            "rule": "True wealth is built across decades, not quarters. Align your capital with irreversible civilizational trends."
        }
    }

    # =========================================================================
    # 3. THE 15 TOP FINANCIAL TITANS / HUMAN BEINGS (GROUPED BY CATEGORY)
    # =========================================================================
    TOP_15_TITANS = {
        # Category 1: Value Investing & Long-Term Capital Allocation
        "buffett": {
            "name": "Warren Buffett",
            "category": "Value Investing & Long-Term Capital Allocation",
            "domain_expertise": "Moat-based corporate equity and structural value investing",
            "analytical_superpower": "Evaluating businesses with durable competitive advantages and calculating long-term compounding potential",
            "professional_role": "Chairman & CEO, Berkshire Hathaway",
            "key_laws": [
                "Rule No. 1: Never lose money. Rule No. 2: Never forget rule No. 1.",
                "Durable Economic Moats: Invest only in companies with pricing power, high return on capital, and wide barriers to entry.",
                "Circle of Competence: Know the boundaries of what you understand and never stray outside them.",
                "Mr. Market is your servant, not your guide: Exploit market emotional swings rather than being infected by them."
            ],
            "bio": "The most successful fundamental investor in history, compounding capital at ~20% annually over six decades through Berkshire Hathaway."
        },
        "marks": {
            "name": "Howard Marks",
            "category": "Value Investing & Long-Term Capital Allocation",
            "domain_expertise": "High-yield debt markets and credit risk management",
            "analytical_superpower": "Reading macroeconomic cycle extremes and executing 'second-level thinking' to buy assets when others panic",
            "professional_role": "Co-Chairman & Co-Founder, Oaktree Capital Management",
            "key_laws": [
                "Second-Level Thinking: First-level asks 'is this a good company?'. Second-level asks 'is everyone expecting it to be great, making the price dangerously high?'.",
                "The Pendulum of Investor Psychology: Markets swing between excessive euphoria (greed) and unwarranted despair (panic). The pendulum always swings back.",
                "Asymmetric Risk Management: Downside risk must be eliminated first; if you take care of the losses, the winners will take care of themselves.",
                "You Can't Predict, But You Can Prepare: Recognize where we are in the cycle and adjust aggressiveness versus defensiveness."
            ],
            "bio": "Author of 'The Most Important Thing' whose memos are required reading for Warren Buffett and institutional allocators globally."
        },
        "lynch": {
            "name": "Peter Lynch",
            "category": "Value Investing & Long-Term Capital Allocation",
            "domain_expertise": "Growth stock selection and retail equity investing",
            "analytical_superpower": "Translating everyday consumer trends into high-yielding, fundamental business opportunities before Wall Street notices",
            "professional_role": "Former Legendary Manager, Fidelity Magellan Fund",
            "key_laws": [
                "Invest in What You Understand: Use your everyday consumer observations to spot early business trends before Wall Street analysts notice.",
                "The PEG Ratio: Price-to-Earnings divided by Earnings Growth rate; PEG < 1.0 represents attractive value with growth.",
                "Categorize Your Companies: Know if you own a Fast Grower (20%+ growth), a Stalwart (10-12%), a Cyclical, a Turnaround, or an Asset Play.",
                "Tenbaggers: Never sell your biggest winners just because they went up 2x; let compounders run as long as fundamentals remain intact."
            ],
            "bio": "Generated a legendary 29.2% annualized return over 13 years managing Fidelity Magellan, author of 'One Up on Wall Street'."
        },
        "smith": {
            "name": "Terry Smith",
            "category": "Value Investing & Long-Term Capital Allocation",
            "domain_expertise": "Concentrated, high-quality global equity investing",
            "analytical_superpower": "Identifying companies with exceptionally high Returns on Capital Employed (ROCE) that don't require heavy debt to grow",
            "professional_role": "Founder & Chief Investment Officer, Fundsmith",
            "key_laws": [
                "The 3-Step Investment Philosophy: 1. Buy good companies. 2. Don't overpay. 3. Do nothing.",
                "High ROCE Without Leverage: Only invest in companies that generate >20-25% Return on Capital Employed organically from intangible assets and consumer loyalty.",
                "Avoid Turnarounds & Cyclicals: Turnarounds rarely turn; quality businesses with high gross margins survive any recession.",
                "Minimize Portfolio Turnover: High trading churn enriches brokers and taxes; real wealth comes from sitting on superior capital compounders."
            ],
            "bio": "Known as the 'English Warren Buffett', who built Fundsmith into one of Europe's most successful mutual funds through concentrated quality investing."
        },

        # Category 2: Global Macroeconomic Strategy & Market Mechanics
        "dalio": {
            "name": "Ray Dalio",
            "category": "Global Macroeconomic Strategy & Market Mechanics",
            "domain_expertise": "Macroeconomic debt cycles and systematic asset allocation",
            "analytical_superpower": "Deconstructing global economic history into algorithmic frameworks to build all-weather portfolios",
            "professional_role": "Founder & Mentor, Bridgewater Associates",
            "key_laws": [
                "The Economic Machine: Driven by 3 main forces: Productivity growth, the Short-Term Debt Cycle (5-8 yrs), and the Long-Term Debt Cycle (75-100 yrs).",
                "All-Weather Risk Parity: Balance risk equally across 4 economic environments: rising growth, falling growth, rising inflation, falling inflation.",
                "Pain + Reflection = Progress: Emotional pain is a signal to stop, reflect on reality, and formulate an objective systematic rule.",
                "Radical Truth and Radical Transparency: Never let ego or false politeness hide the fundamental facts of a business or portfolio."
            ],
            "bio": "Founder of Bridgewater Associates, the largest hedge fund in history, author of 'Principles' and 'Principles for Dealing with the Changing World Order'."
        },
        "druckenmiller": {
            "name": "Stanley Druckenmiller",
            "category": "Global Macroeconomic Strategy & Market Mechanics",
            "domain_expertise": "Multi-asset global macro trading",
            "analytical_superpower": "Recognizing seismic shifts in central bank liquidity and aggressively sizing bets across currencies, bonds, and equities",
            "professional_role": "Founder, Duquesne Family Office",
            "key_laws": [
                "Liquidity Drives Markets, Not Earnings: Central bank liquidity, money supply, and Fed policy determine market direction far more than corporate quarterly reports.",
                "Aggressive Bet Sizing: When you have tremendous conviction on a trade, put all your eggs in one basket and watch that basket very carefully.",
                "Preserve Capital First: The way you build long-term returns is through preservation of capital and home runs; don't take 50/50 mediocre bets.",
                "Fast Reversal of Opinion: Have zero emotional pride in your previous thesis; when the macroeconomic facts change, flip your position instantly."
            ],
            "bio": "Compiled a 30-year track record averaging ~30% annualized returns with zero down years at Duquesne Capital and Soros's Quantum Fund."
        },
        "el_erian": {
            "name": "Mohamed El-Erian",
            "category": "Global Macroeconomic Strategy & Market Mechanics",
            "domain_expertise": "Sovereign debt, monetary policy, and emerging markets",
            "analytical_superpower": "Analyzing central bank behaviors (e.g., US Fed) and predicting regulatory policy impact on global market stability",
            "professional_role": "Chief Economic Advisor, Allianz; President, Queens' College, Cambridge",
            "key_laws": [
                "The New Normal & Structural Stagnation: Central banks cannot solve structural growth problems with monetary easing alone.",
                "T-Junction Scenarios: Markets often face binary paths where staying in the middle is impossible; prepare for non-linear policy pivots.",
                "Sovereign Debt Capacity & Emerging Market Spreads: Watch sovereign debt sustainability, foreign exchange reserves, and capital flight dynamics.",
                "Resilience Over Optimization: Do not over-optimize a portfolio for a single perfect forecast; build operational resilience to withstand policy shocks."
            ],
            "bio": "Former CEO & Co-CIO of PIMCO, leading voice on global monetary economics, sovereign debt, and international financial architecture."
        },
        "jones": {
            "name": "Paul Tudor Jones",
            "category": "Global Macroeconomic Strategy & Market Mechanics",
            "domain_expertise": "Technical trading, commodities, and macro futures",
            "analytical_superpower": "Reading market momentum, volume data, and human behavior to execute disciplined, asymmetric risk-reward trades",
            "professional_role": "Founder & Chief Investment Officer, Tudor Investment Corporation",
            "key_laws": [
                "The 5:1 Asymmetric Risk-Reward Rule: Risk $1 to make $5. With this math, you can be wrong 80% of the time and still not lose money.",
                "The 200-Day Moving Average Defense: Never trade or hold long positions below a 200-day moving average. It protects you from catastrophic bear markets.",
                "Defense First: Don't focus on making money; focus on protecting what you have. Spend every trading day thinking about where your risk lies.",
                "Losers Average Losers: Never add to a losing trade or average down on speculative futures; honor your stop-losses ruthlessly."
            ],
            "bio": "Legendary macro trader who predicted and profited from the 1987 Black Monday crash, achieving decades of consistent double-digit returns."
        },

        # Category 3: Corporate Valuation & Quantitative Finance
        "damodaran": {
            "name": "Aswath Damodaran",
            "category": "Corporate Valuation & Quantitative Finance",
            "domain_expertise": "Corporate finance and business valuation",
            "analytical_superpower": "Demystifying corporate balance sheets, modeling cash flows under uncertainty, finding intrinsic value of tech/legacy companies",
            "professional_role": "Professor of Finance, NYU Stern School of Business",
            "key_laws": [
                "Cash is Fact, Profit is an Opinion: Focus exclusively on Free Cash Flow to the Firm (FCFF = NOPAT - Reinvestment).",
                "WACC & Country Risk: In emerging markets like India, Cost of Capital must reflect the sovereign risk-free yield plus Equity Risk Premium.",
                "The Terminal Growth Boundary: A company's terminal growth rate cannot mathematically exceed the long-term risk-free GDP growth rate of its economy.",
                "Narrative and Numbers: A valuation without a believable corporate narrative is just math; a narrative without numbers is pure fiction."
            ],
            "bio": "World-renowned valuation authority whose open-source global databases and textbooks define modern Discounted Cash Flow (DCF) modeling."
        },
        "asness": {
            "name": "Cliff Asness",
            "category": "Corporate Valuation & Quantitative Finance",
            "domain_expertise": "Systematic and factor-based quantitative investing",
            "analytical_superpower": "Using advanced mathematics and massive historical datasets to isolate market anomalies like value, momentum, and quality",
            "professional_role": "Co-Founder & Principal, AQR Capital Management",
            "key_laws": [
                "Factor Investing Alpha: Systematic excess returns come from measurable factors: Value (cheap vs fundamental), Momentum (trend persistence), Carry, and Defensive Quality.",
                "Value and Momentum are Best Friends: Value investing and Momentum investing have strong negative correlation; combining them produces vastly superior risk-adjusted Sharpe ratios.",
                "Sin a Little, Don't Sin a Lot: Avoid market timing factor tilts; maintain disciplined, steady exposure across all weather conditions.",
                "Overfitting is the Enemy of Quants: If you torture historical data long enough, it will confess to anything. Rely only on economically rational anomalies."
            ],
            "bio": "Pioneer of quantitative factor investing, student of Eugene Fama, managing tens of billions in systematic quantitative portfolios at AQR."
        },

        # Category 4: Institutional Risk & Scale Management
        "fink": {
            "name": "Larry Fink",
            "category": "Institutional Risk & Scale Management",
            "domain_expertise": "Institutional asset management and systemic risk modeling",
            "analytical_superpower": "Constructing digital risk infrastructure (Aladdin platform) capable of managing trillions in global capital",
            "professional_role": "Chairman & CEO, BlackRock",
            "key_laws": [
                "The Power of the Aladdin Platform: Enterprise risk management must aggregate credit, liquidity, and currency exposures across millions of securities in real time.",
                "Low-Cost Passive Scale: Democratize investing through ultra-low-cost index ETFs (iShares), allowing compound interest to work for everyday investors.",
                "Long-Horizon Infrastructure & Transition Capital: Capital allocation is shifting decisively into energy transition, digital data centers, and power grids.",
                "Corporate Stewardship: Companies must demonstrate durable value creation for shareholders and broader society to command institutional capital."
            ],
            "bio": "Co-founder of BlackRock, growing it from a small fixed-income boutique into the world's largest asset manager with $10.5+ Trillion in AUM."
        },
        "dimon": {
            "name": "Jamie Dimon",
            "category": "Institutional Risk & Scale Management",
            "domain_expertise": "Commercial banking and corporate liquidity management",
            "analytical_superpower": "Maintaining an unassailable 'fortress balance sheet' to protect capital through recessions and geopolitical crises",
            "professional_role": "Chairman & CEO, JPMorgan Chase",
            "key_laws": [
                "The Fortress Balance Sheet: Maintain excess Tier 1 common equity, conservative underwriting, and deep cash reserves so the institution can withstand any economic crisis.",
                "Counter-Cyclical Opportunism: When an economic panic causes competitor banks to fail, a fortress balance sheet allows you to acquire pristine assets at pennies on the dollar.",
                "Stress-Testing Beyond Regulatory Minimums: Model multi-standard-deviation geopolitical and interest-rate shocks before they happen.",
                "No Excuses Leadership: Acknowledge mistakes immediately, eliminate bureaucratic bloat, and run your company with extreme operational discipline."
            ],
            "bio": "Longest-tenured leader of JPMorgan Chase, who steered the bank through the 2008 Financial Crisis and 2023 regional banking turmoil without government bailouts."
        },
        "griffin": {
            "name": "Ken Griffin",
            "category": "Institutional Risk & Scale Management",
            "domain_expertise": "Quantitative market-making and multi-strategy hedge fund trading",
            "analytical_superpower": "Engineering high-frequency trading algorithms and low-latency infrastructure to capture micro-inefficiencies in global liquidity",
            "professional_role": "Founder & CEO, Citadel and Citadel Securities",
            "key_laws": [
                "Multi-Strategy Pod Risk Boundaries: Operate independent investment pods across equities, commodities, and fixed income with rigid stop-loss risk boundaries.",
                "Extreme Technological & Execution Advantage: Invest hundreds of millions into ultra-low-latency computing and market microstructure simulation.",
                "Continuous Liquidity Provision: Provide continuous two-sided liquidity across global exchanges, profiting from the bid-ask spread through the law of large numbers.",
                "Relentless Talent & Performance Culture: Allocate capital immediately to winning models and cut underperforming strategies without hesitation."
            ],
            "bio": "Started trading convertible bonds from his Harvard dorm room in 1987, building Citadel into the most profitable hedge fund in history and Citadel Securities into a global market maker."
        },
        "tepper": {
            "name": "David Tepper",
            "category": "Institutional Risk & Scale Management",
            "domain_expertise": "Distressed debt and special situations",
            "analytical_superpower": "Spotting massive valuation disconnects in bankrupt, restructuring, or panicked corporate credit structures",
            "professional_role": "Founder, Appaloosa Management",
            "key_laws": [
                "Don't Fight the Fed: When central banks open the monetary spigots and inject liquidity, step in aggressively and buy risk assets.",
                "Buy Panic in Senior Claims: When a company or financial system faces crisis, buy the senior debt or preferred equity where capital is protected by tangible assets.",
                "Patience at the Bottom: Wait until forced sellers have exhausted their selling, then buy with massive asymmetric upside.",
                "Keep Emotions Cool Under Fire: The greatest fortunes are made when headlines are terrifying and investors are dumping assets in despair."
            ],
            "bio": "Founder of Appaloosa Management, legendary distressed debt investor who generated billions buying banks at the depth of the 2008 crisis."
        },

        # Category 5: Behavioral Economics & Finance Psychology
        "housel": {
            "name": "Morgan Housel",
            "category": "Behavioral Economics & Finance Psychology",
            "domain_expertise": "Behavioral finance and financial history",
            "analytical_superpower": "Analyzing how human ego, greed, and fear impact financial decisions, rather than just cold spreadsheet data",
            "professional_role": "Partner, Collaborative Fund; Bestselling Author ('The Psychology of Money')",
            "key_laws": [
                "Behavior Beats Intelligence: Doing well with money has a little to do with how smart you are and a lot to do with how you behave.",
                "The Goal is Independence, Not Status: True wealth is what you don't spend; the highest form of wealth is the ability to wake up every morning and say 'I can do whatever I want today'.",
                "Room for Error (The Margin for Being Wrong): The most important part of every plan is planning on your plan not going according to plan.",
                "Reasonable Over Rational: Do not aim to be cold-bloodedly rational on a spreadsheet; aim to be reasonable so you can sleep peacefully at night and stick to your strategy."
            ],
            "bio": "Partner at Collaborative Fund, two-time Best in Business award winner, and author of the global mega-bestseller 'The Psychology of Money' (translated into 50+ languages)."
        }
    }

    # =========================================================================
    # 4. THE 7 MASTER CODIFIED FINANCIAL BOOKS (5,053 PAGES)
    # =========================================================================
    CODIFIED_BOOKS_VAULT = {
        "damodaran_valuation": {
            "title": "Investment Valuation: Tools and Techniques for Determining the Value of Any Asset (3rd Edition)",
            "author": "Aswath Damodaran (NYU Stern)",
            "pages": 949,
            "core_principles": [
                "Cash Flow is Fact, Accounting Profit is an Opinion (FCFF = NOPAT - Reinvestment)",
                "WACC & Equity Risk Premiums: Country Risk Premiums for emerging markets like India",
                "Terminal Growth Rate cannot exceed risk-free long-term sovereign GDP growth",
                "The Value of Intangibles, R&D Capitalization, and Brand Moats"
            ],
            "cross_links": "Linked to NYU Stern & Titan Aswath Damodaran"
        },
        "mckinsey_valuation": {
            "title": "Valuation: Measuring and Managing the Value of Companies (7th Edition)",
            "author": "McKinsey & Company (Tim Koller, Marc Goedhart, David Wessels)",
            "pages": 862,
            "core_principles": [
                "The Fundamental Law of Value Creation: Value is driven by ROIC and Growth; Growth creates value only if ROIC > WACC",
                "The Key Value Driver Equation: Value = NOPAT * (1 - g/ROIC) / (WACC - g)",
                "Economic Profit (EVA): True economic value added = Invested Capital * (ROIC - WACC)",
                "Continuing Value Discipline: Eliminating unrealistic perpetuity reinvestment assumptions"
            ],
            "cross_links": "Linked to McKinsey & Company & Tim Koller"
        },
        "security_analysis": {
            "title": "Security Analysis: Principles and Technique (7th Edition)",
            "author": "Benjamin Graham & David L. Dodd (Foreword by Seth Klarman, Warren Buffett)",
            "pages": 1135,
            "core_principles": [
                "The Margin of Safety: Demanding a 25%-35% discount between market price and conservative intrinsic asset value",
                "Net-Net Working Capital Floor (NCAV = Current Assets - Total Liabilities)",
                "Senior Claim Protection: Auditing debt covenants and liquidation seniority hierarchy",
                "Normalized Earning Power: Stripping out peak cyclical earnings across full 7-10 year economic cycles"
            ],
            "cross_links": "Linked to Columbia Business School & Warren Buffett"
        },
        "corporate_finance": {
            "title": "Principles of Corporate Finance (7th Edition)",
            "author": "Richard A. Brealey & Stewart C. Myers (LBS & MIT Sloan)",
            "pages": 1062,
            "core_principles": [
                "The Net Present Value (NPV) Decision Rule: Value additivity of independent cash flow projects",
                "Pecking Order Theory (Myers): Companies fund operations through internal cash > safe debt > equity dilution",
                "Modigliani-Miller Propositions: Impact of corporate taxes and financial distress costs on debt-equity ratio",
                "Real Options Valuation: Valuing management flexibility to expand, abandon, or defer investments"
            ],
            "cross_links": "Linked to London Business School, MIT Sloan, Richard Brealey & Stewart Myers"
        },
        "quant_ml": {
            "title": "Advances in Financial Machine Learning",
            "author": "Marcos López de Prado (Cornell University & Quant Pioneer)",
            "pages": 489,
            "core_principles": [
                "Half-Kelly Capital Allocation: Sizing positions via fractional Kelly criterion to eliminate volatility ruin",
                "Triple Barrier Method: Dynamic exit barriers for profit take, stop-loss floor, and time expiration",
                "Fractional Differentiation: Preserving long-term price memory while achieving mathematical stationarity",
                "Deflated Sharpe Ratio: Correcting for backtest overfitting, false discoveries, and multiple testing trials"
            ],
            "cross_links": "Linked to Renaissance Technologies, Two Sigma & Citadel Quantitative Pod Architecture"
        },
        "financial_shenanigans": {
            "title": "Financial Shenanigans: How to Detect Accounting Gimmicks & Fraud in Financial Reports (4th Edition)",
            "author": "Howard M. Schilit & Jeremy Perler",
            "pages": 312,
            "core_principles": [
                "7 Earnings Manipulation Shenanigans (Recording revenue too soon, bogus revenue, one-time gains)",
                "Cash Flow Shenanigans: Shifting financing cash flows into operating cash flows or accelerating collections",
                "Beneish M-Score & Sloan Accrual Anomaly: Detecting when accruals outpace cash collections",
                "Working Capital Divergence: DSO and inventory spiking ahead of sales signals channel stuffing"
            ],
            "cross_links": "Forensic Accounting Shield used by Institutional Activist Funds (Elliott Management)"
        },
        "most_important_thing": {
            "title": "The Most Important Thing Illuminated: Uncommon Sense for the Thoughtful Investor",
            "author": "Howard Marks (Oaktree Capital Management)",
            "pages": 244,
            "core_principles": [
                "Second-Level Thinking: Factoring in market consensus expectations vs reality",
                "The Pendulum of Investor Psychology: Oscillating between excessive greed and excessive fear",
                "Asymmetric Risk Management: Downside elimination produces superior long-term results; winners take care of themselves",
                "Patient Opportunism: Waiting for forced sellers in a market liquidity crisis"
            ],
            "cross_links": "Linked to Oaktree Capital Management & Titan Howard Marks"
        }
    }

    # =========================================================================
    # 5. THE 4 EMPIRICAL DATASETS & QUANT ARCHIVES
    # =========================================================================
    EMPIRICAL_DATASETS_VAULT = {
        "jay_ritter_ipos": {
            "name": "Professor Jay Ritter IPO Database (University of Florida)",
            "files": ["jay_ritter_ipos_underpricing.pdf", "jay_ritter_ipos_long_run_returns.pdf", "jay_ritter_ipos_vc_backed.pdf", "jay_ritter_ipos_tech.pdf", "jay_ritter_ipo_statistics.pdf"],
            "coverage": "45+ years of global & Indian IPO empirical performance (1980-2026)",
            "laws": "First-day underpricing anomalies (listing day pops), 3-year post-IPO underperformance curve, and OFS promoter exit dilution traps."
        },
        "damodaran_sector_data": {
            "name": "Damodaran Global Sector Valuation & Multiples Archive (NYU Stern)",
            "files": ["operating_margins_by_sector.xls", "cost_of_capital_by_sector.xls", "capex_and_reinvestment_by_sector.xls", "valuation_multiples_by_sector.xls", "country_equity_risk_premiums.xls", "compiled_sector_data.json"],
            "coverage": "6,000+ public firms across 94 global & emerging market sectors",
            "laws": "Industry benchmark WACCs, EV/EBITDA, P/E multiples, Net Margins, Reinvestment Rates, and Sovereign Equity Risk Premiums."
        },
        "fred_macroeconomic": {
            "name": "Federal Reserve Economic Data (FRED)",
            "files": ["fred_10y_treasury_yield.csv", "fred_fed_funds_rate.csv"],
            "coverage": "Decades of US 10-Year Treasury Yields, benchmark risk-free curves, and Fed Funds interest rate cycles",
            "laws": "Interest rates as the gravitational anchor of global equity valuation multiples."
        },
        "fama_french_factors": {
            "name": "Fama-French Multi-Factor Asset Pricing Data (University of Chicago)",
            "files": ["F-F_Research_Data_Factors.csv"],
            "coverage": "Historical daily and monthly factor returns for Market Beta, Small-Minus-Big (SMB), and High-Minus-Low (HML) Value factor",
            "laws": "Systematic factor pricing vs idiosyncratic single-stock alpha."
        }
    }

    # =========================================================================
    # 6. CURRENT REAL-WORLD SITUATION & TOP NEWS (SEP-OCT 2026)
    # =========================================================================
    @classmethod
    def get_real_world_market_briefing(cls) -> str:
        """Detailed real-world macroeconomic and market briefing for Sep-Oct 2026."""
        return """### 🌐 Current World & Market Situation Briefing (Sep–Oct 2026)

Here is the real-time institutional macroeconomic intelligence across India and global markets:

#### 1. 🇮🇳 India Macroeconomic Fortress
• **GDP Growth Leadership**: The Indian economy continues to be the world's fastest-growing major economy, clocking an annualized GDP growth rate of **7.2%+**, propelled by robust domestic consumption and private capital formation.
• **The Retail SIP Liquidity Moat**: Domestic retail Systematic Investment Plans (SIPs) in mutual funds are consistently surpassing **₹24,000+ Crore per month**. This creates an unprecedented domestic liquidity cushion that absorbs Foreign Institutional Investor (FII) selling during global volatility.
• **Monetary Policy & Inflation**: The Reserve Bank of India (RBI) maintains a balanced, steady interest rate stance, with Consumer Price Index (CPI) inflation contained within the RBI's target band (~3.8%–4.2%).
• **Capex Super-Cycle**: Unprecedented government and private sector capital deployment across **Indian Railways modernization, Defense indigenization ('Make in India' with HAL/BEL), Renewable Clean Energy (Solar & Green Hydrogen), and Electronics/Semiconductor PLI schemes**.

#### 2. 🌍 Global Macro & Geopolitics
• **US Federal Reserve Monetary Easing**: The US Fed is in an active interest rate easing cycle, lowering benchmark borrowing costs. This is expanding global liquidity, softening the US Dollar index, and directing emerging market capital flows into high-growth economies like India.
• **The 'China + 1' Supply Chain Realignment**: Global multinationals are accelerating their supply chain de-risking away from China, directly benefiting Indian electronics manufacturing (e.g., Apple iPhone export surges via Tata Electronics and Foxconn India) and specialty chemical exporters.
• **AI Infrastructure Mega-Capex**: Global tech hyperscalers (Nvidia, Microsoft, Alphabet, Amazon, Meta) are investing hundreds of billions into next-generation AI data centers, specialized silicon (Blackwell architectures), and power grid modernization.

#### 3. 🚀 Indian Primary Markets (Active IPOs & Exchange Action)
• **Active Indian IPOs**: High investor activity across **Moneyview Limited** (Fintech lending, 38%+ GMP, strong listing gains), **Runwal Enterprises** (Real Estate expansion), and **AceVector/Snapdeal** (E-Commerce, cautious stance due to high OFS).
• **Market Valuation Realism**: The Nifty 50 trades around fair-value historical P/E bands (~21x–23x), rewarding companies with demonstrable cash flow, high Return on Invested Capital (ROIC), and clean forensic balance sheets while penalizing loss-making speculative hype."""

    # =========================================================================
    # 4. GIBBERISH & KEYBOARD MASHING DETECTOR
    # =========================================================================
    @classmethod
    def is_random_gibberish(cls, text: str) -> bool:
        """
        Intelligently detects accidental keypresses, keyboard mashing, or random typing
        (e.g., 'asdfghjkl', 'qwertyuiop', 'hfkjsdhfkjd', 'zzzzzzz', '11111111').
        Guarantees legitimate financial tickers, acronyms, and questions are NEVER misidentified.
        """
        s = text.strip().lower()
        if not s:
            return False

        # If it contains clear financial or conversational intent words, it's NOT gibberish
        valid_intents = {
            "stock", "share", "ipo", "buy", "sell", "hold", "invest", "money", "nifty", "sensex",
            "reliance", "tata", "sbi", "hdfc", "infosys", "zomato", "itc", "apple", "nvidia",
            "how", "what", "which", "where", "why", "who", "when", "can", "should", "tell",
            "hi", "hello", "hey", "help", "good", "bad", "loss", "profit", "news", "today",
            "market", "crash", "fall", "sip", "fund", "gmp", "price", "dcf", "pe", "wacc",
            "buffett", "marks", "lynch", "smith", "dalio", "druckenmiller", "erian", "jones",
            "damodaran", "asness", "fink", "dimon", "griffin", "tepper", "housel",
            "harvard", "stanford", "mit", "oxford", "chicago", "wharton", "upenn", "cambridge",
            "lse", "berkeley", "nus", "nyu", "columbia", "yale", "lbs", "imperial"
        }
        words = re.findall(r'[a-z]+', s)
        if any(w in valid_intents for w in words):
            return False

        # Clean string of only alphanumeric characters
        alpha = re.sub(r'[^a-z0-9]', '', s)
        if len(alpha) == 0:
            return True

        # Any greeting elongation (e.g. 'hiiiii', 'heeeey', 'helloooo', 'yo', 'sup') is NOT gibberish
        if re.match(r'^(h+i+|h+e+y+|h+e+l+o+|y+o+|s+u+p+|w+a+s+u+p+)$', alpha):
            return False

        # Check for repetitive identical characters (e.g., 'aaaaaa', '.....', '111111')
        if len(alpha) >= 4 and len(set(alpha)) <= 2:
            return True

        # Common keyboard row walk / mash patterns
        keyboard_walks = [
            "asdf", "sdfg", "dfgh", "fghj", "ghjk", "hjkl", "jkl;",
            "qwerty", "werty", "ertyu", "rtyui", "tyuio", "yuiop",
            "zxcvb", "xcvbn", "cvbnm",
            "12345", "23456", "34567", "45678", "56789",
            "poiuy", "lkjhg", "mnbvc", "qazwsx", "wsxedc"
        ]
        for kw in keyboard_walks:
            if kw in alpha:
                return True

        # Check for long consonant clusters without vowels (e.g. 'hfkjsdhfk', 'bcdfghjk')
        if len(alpha) >= 6 and not any(v in alpha for v in "aeiouy"):
            return True

        # Very high consonant-to-vowel ratio in a single long pseudo-word
        if len(alpha) >= 8 and len(words) == 1:
            vowels_count = sum(1 for c in alpha if c in "aeiouy")
            if vowels_count <= 1:
                return True

        return False

    @classmethod
    def get_gibberish_response(cls, raw_text: str) -> str:
        """Warm, playful, and human response to accidental keyboard mashing."""
        return f"""### 😄 Haha, looks like a little keyboard fun!

It seems like **"{raw_text}"** was an accidental keypress or a quick tap across the keyboard! 

Don't worry at all — I'm right here and ready whenever you are. Whether you'd like to:
• 🚀 Check **"which IPO to apply for today"**
• 📊 Ask **"what stocks should I buy for long term?"**
• 🔍 Audit a specific company like **Tata Motors, Reliance, or Zomato**
• 🧠 Explore how **Warren Buffett, Howard Marks, or Stanley Druckenmiller** analyze markets
• 🏛️ Learn from the financial breakthroughs of **Harvard, MIT, Stanford, or Wharton**
• 🌍 Get the **latest world and Indian market news**

What would you like to explore today?"""

    # =========================================================================
    # 5. EMOTIONAL INTELLIGENCE & PSYCHOLOGY ENGINE
    # =========================================================================
    @classmethod
    def detect_and_handle_emotions(cls, raw: str) -> Optional[str]:
        """
        Empathetic, human-centric emotional intelligence.
        Reassures panic, grounds greed, clarifies confusion, and guides recovery.
        """
        # 1. FEAR, LOSS, ANXIETY & MARKET PANIC
        fear_signals = [
            "i am scared", "i am afraid", "losing money", "lost money", "lost all my money",
            "big loss", "market is falling", "market crash", "everything is red", "panic",
            "depressed", "anxious", "stress", "stressed", "family tension", "ruined",
            "darr lag raha", "paisa doob gaya", "loss ho gaya", "kya karu market gir raha"
        ]
        if any(f in raw for f in fear_signals):
            return """### 🧘 Take a Deep Breath: You Are Not Alone, and This is Natural

I hear the stress in your words, and I want you to know: **it is completely normal to feel an ache in your stomach when the market turns red.** Even legendary investors like Warren Buffett and Howard Marks experienced times when their portfolios dropped 50% on paper.

As **Morgan Housel** reminds us in *The Psychology of Money*:
> *"Doing well with money isn't about being extraordinarily smart; it's about being able to control your behavior when everyone else is losing their heads."*

Here is the perspective from the greatest financial minds to help you find your footing:

1. **A Paper Loss is Not a Permanent Loss**:
   • Stock market quotes fluctuate daily like Howard Marks' pendulum. But if you own shares in fundamentally profitable, debt-free companies, the business itself continues to generate cash every single day.
   • The only way a temporary market drop becomes a permanent loss is if you panic-sell at the exact bottom.

2. **The Golden Rule of Second-Level Thinking (Howard Marks)**:
   • First-level thinkers panic and say: *"Prices are falling, I must sell everything before it hits zero."*
   • Second-level thinkers say: *"Mr. Market is currently having an emotional breakdown and offering wonderful Indian companies at a massive discount."*

3. **Your Immediate Action Plan**:
   • **Step 1**: Step away from the screen for a couple of hours. Constantly refreshing red candles only fuels anxiety.
   • **Step 2**: Check if you have invested emergency funds. (If you haven't, you have time on your side).
   • **Step 3**: Let's audit the exact stocks you hold together. If the company is fundamentally sound (clean balance sheet, positive cash flow), time will reward your patience.

Would you like to tell me which specific stocks you're holding so we can look at their real business health together calmly?"""

        # 2. GREED, FOMO, GET-RICH-QUICK, OPTIONS TRADING URGES
        greed_signals = [
            "get rich quick", "fast money", "10x in 1 week", "multibagger in 1 month",
            "option trading", "call put", "f&o", "intraday quick profit", "borrow money to invest",
            "take loan to invest", "quick 1 lakh", "double my money fast", "paisa double"
        ]
        if any(g in raw for g in greed_signals):
            return """### 🛡️ An Honest Institutional Word: The Truth About Fast Money

I completely understand the excitement of wanting to grow your money rapidly. Financial freedom is an amazing goal, and we all want to reach it as quickly as possible.

However, as your institutional guardian, I owe you absolute truth rather than sweet lies:

1. **The Official Truth on Options & Intraday Trading (SEBI Study)**:
   • According to official data from the Securities and Exchange Board of India (SEBI), **over 93% of retail traders lose money in Futures & Options (F&O)**, with the average loss exceeding ₹1.25 Lakh per person.
   • Options trading is a zero-sum game with severe time decay (Theta) stacked against you. You are trading against automated supercomputers and high-frequency algorithms engineered by people like Ken Griffin at Citadel.

2. **Never Borrow Money (Take a Loan) to Invest**:
   • Stanley Druckenmiller and Paul Tudor Jones both emphasize: capital preservation comes first. Borrowed money forces you to exit at the worst possible time when volatility strikes, destroying your financial peace.

3. **How Real Wealth is Actually Built (Terry Smith & Warren Buffett)**:
   • Terry Smith built billions by simply: *1. Buying good companies. 2. Not overpaying. 3. Doing nothing.*
   • Compounding at 15%–18% per year in high-ROCE compounders turns ₹50,000 into multi-lakh wealth without sleepless nights.

Let's build you a rock-solid investment portfolio that makes you wealthy permanently, without risking your hard-earned savings. Shall we start?"""

        # 3. CONFUSION, BEGINNERS, SMALL CAPITAL & OVERWHELM
        beginner_signals = [
            "i am beginner", "new to market", "don't know anything", "i am confused",
            "where do i start", "how to begin", "small money", "salary is small",
            "guide me", "step by step", "first time", "kuch nahi pata", "kaise shuru kare"
        ]
        if any(b in raw for b in beginner_signals):
            return """### 🌱 Welcome! Investing is Simpler Than You Think

Don't worry at all! The financial industry often uses complicated jargon (DCF, WACC, Beta, EBITDA) to make things sound intimidating. But as **Peter Lynch** and **Morgan Housel** teach, at its heart, building wealth is very straightforward.

Here is the **3-Step Institutional Blueprint** for every beginner starting today:

1. **Step 1: Build Your Armor (Safety First)**
   • Keep 3 to 6 months of living expenses safely in a savings account or Fixed Deposit as an Emergency Fund.
   • Get a basic term insurance policy and health insurance so a medical emergency never forces you to touch your investments.

2. **Step 2: Automate Wealth Compounding (The SIP Route)**
   • Start a monthly Systematic Investment Plan (SIP) in a **Nifty 50 Index Fund** or a **Flexi-Cap Fund** with even ₹1,000 or ₹2,000.
   • When you buy the Nifty 50, you instantly become an owner of India's top 50 corporate giants (Reliance, Tata, HDFC, Infosys, etc.). As India grows, your wealth grows automatically.

3. **Step 3: Tactical Stock & IPO Investments**
   • Once your SIP baseline is running, use spare savings to buy high-quality companies at a discount (like Tata Motors Passenger Vehicles) or apply for vetted, high-GMP IPOs (like Moneyview) for listing gains.

Tell me: how much capital or monthly savings are you looking to start with? I will give you an exact, tailored allocation plan!"""

        return None
