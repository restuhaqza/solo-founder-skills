# Ops & Legal Checklist for the Solo Founder

> **Human-review boundary.** Everything in this file is a *prompt and a first draft*, not legal, tax, or entity advice. Choosing an entity, filing forms, writing a contract, and deciding what you owe are decisions you own — with a lawyer or accountant where the stakes are real. Do not treat any line here as a filing instruction, and never sign or file AI-drafted text unreviewed. When a specific in this file conflicts with what a professional tells you, the professional is right and this file is out of date.

**Contents**
1. Essential before launch vs what can wait
2. Entity: sole prop, single-member LLC, or corporation
3. The EIN
4. Separate bank account and the commingling trap
5. Terms of Service, Privacy Policy, and DPAs
6. Tax registration and dates
7. If you are a non-US owner of a US LLC: Form 5472
8. Working the checklist

---

## 1. Essential before launch vs what can wait

The trap is treating every legal item as a launch blocker. Most are not. Separate the things that expose you *now* from the things that can wait until a customer, a jurisdiction, or a dollar amount makes them real.

**Essential before you take money or personal data:**

- [ ] A way to take payment that matches a real, identifiable business (see §4).
- [ ] A **Terms of Service** and a **Privacy Policy** on the site — even short ones — once you collect data or charge customers.
- [ ] A data-handling plan: what you collect, where it lives, who can see it, and how a customer deletion request would work.
- [ ] Basic liability thinking: if your product can cause financial or personal harm, get advice before launch, not after.

**Can usually wait, but plan them:**

- [ ] A trademark search and registration — worth doing once the name is settled and you are committing to it, not on day one.
- [ ] A full **DPA** (data processing agreement) — often only needed when a business customer asks for one.
- [ ] Formal contracts with contractors — get a simple written agreement early, but a bespoke one can wait.
- [ ] Operating agreements, cap tables, and anything equity-related — these matter when equity is actually being issued.

When in doubt, ask: *what is my actual downside this month?* Address that first.

## 2. Entity: sole prop, single-member LLC, or corporation

There is no universal right answer; the choice trades **simplicity and cost** against **liability protection and tax treatment**. The three common shapes for a solo software business:

- **Sole proprietorship** — the default if you just start. Simplest and cheapest: no separate entity, but **no liability separation** between you and the business, and personal assets are exposed. Fine for a small experiment with little risk; thin once money and customers are real.
- **Single-member LLC** — a separate legal entity, common for solo founders because it separates business from personal for liability purposes (see §4) while defaulting to simple pass-through tax treatment in many places. Adds a filing and often a small annual fee; the liability shield is the main reason people choose it.
- **Corporation (e.g. C-corp)** — usually only when raising venture capital, issuing equity broadly, or where a specific tax or investor structure requires it. More formalities and cost; overkill for most bootstrapped solo businesses.

The right call depends on your jurisdiction, your risk, and your plans — which is exactly why this is a decision to make **with an accountant or lawyer**, not from a checklist. What this skill does is make sure you *ask the question*, and know that "I'll deal with it later" is itself a choice with consequences.

## 3. The EIN

An **EIN** (Employer Identification Number) is a US tax ID for a business — distinct from your personal Social Security Number. A business often needs one to open a business bank account, file certain returns, or work with payment processors and platforms. Applying is generally free and straightforward through the official IRS channel.

Practical notes:

- **Use the official government source.** Services that charge to "get you an EIN" are usually just filling the same free form.
- **A sole proprietor can often use an EIN or a personal ID**, but using an EIN keeps your personal number out of business paperwork and is the cleaner separation.
- **Keep the number with your entity records**, and use it consistently on filings and accounts.

Confirm the current process and requirements for your situation before applying; forms and portals change.

## 4. Separate bank account and the commingling trap

Open a **business bank account** (and ideally a business card) and run *all* business money through it. This is the operational half of whatever entity you chose.

- **Why it matters:** if you formed an LLC for liability protection, that protection is undermined when you treat the business and yourself as one pile of money. Courts and counterparties have historically used **commingled funds** as evidence that the entity was not really separate — which can expose personal assets the entity was meant to protect. Even outside the US, clean separation makes everything downstream simpler.
- **The rule of thumb:** business money only touches business accounts. Pay yourself a clear, labelled **owner draw**. Do not pay personal expenses from the business account, and do not run business costs through a personal card.
- **Keep the paperwork:** receipts, a note on any transfer between accounts, and a reason for each draw.

A separate account costs almost nothing and removes a whole class of future problems.

## 5. Terms of Service, Privacy Policy, and DPAs

Once you collect data or money, you have obligations, and the documents are how you set expectations and answer regulators and customers.

- **Terms of Service (ToS)** — the contract with your users: what the service is, acceptable use, payment and refund terms, limitation of liability, and how disputes are handled.
- **Privacy Policy** — what personal data you collect, why, where it is stored, who it is shared with, how long you keep it, and how someone can access or delete it. Privacy law (GDPR, CCPA/CPRA, and others) imposes real requirements on businesses that touch EU or California residents; the specifics depend on your users and location.
- **DPA (Data Processing Agreement)** — a contract governing how you process data *on behalf of* a business customer. Usually requested by larger or more regulated customers; not always needed at the start.

**How to use an AI draft here:** it is fine to draft comprehension and a first pass of these documents with an agent — but they are legal instruments, and the wording carries consequences. Have a professional review anything that will be relied on, and never copy another site's policy wholesale (it will not match your data practices). Generate a first draft, list the open questions, and route it to review before you publish.

## 6. Tax registration and dates

Tax has two parts: **registering** with the relevant authorities, and **paying on the right dates**. Both vary by country, state, and entity, so treat this as a to-do list to confirm, not a calendar to trust blindly.

- **Registration** — depending on your location, you may need a tax registration number, to register for VAT/GST/sales tax, and to register as an employer if you pay anyone. Payment processors and merchant-of-record platforms may withhold or remit some of this for you.
- **Estimated / quarterly payments** — many jurisdictions expect periodic payments rather than one annual bill, precisely so the bill never becomes a shock. This is the reason for the set-aside habit in `references/runway-and-finance.md`.
- **Deadlines** — put the dates that apply to *you* in your own calendar, sourced from the official tax authority or your accountant, and set a reminder two weeks before each.

**Ask an accountant to confirm your registration obligations and dates before your first filing.** The cost of the question is trivial next to the cost of a missed deadline or a wrong filing.

## 7. If you are a non-US owner of a US LLC: Form 5472

If you are a non-US person who owns a US single-member LLC, there is an information-reporting obligation many owners have never heard of: **Form 5472**, filed together with a **pro-forma Form 1120**, for the LLC's reportable transactions with its foreign owner. It is an *information* return — it does not necessarily mean you owe US tax — but failing to file it carries a penalty that is **commonly cited at around $25,000**, and it is assessed per form, per year, until cured.

What to take from this:

- **It is a filing you must know about, not one you can infer.** A US LLC can trigger US filing duties even when you live and work abroad.
- **The penalty for silence is severe relative to the cost of compliance.** Many owners only discover the obligation when a penalty notice arrives.
- **This is exactly the kind of item to hand to a professional who handles non-US owners of US LLCs.** Do not attempt to determine your own filing position from this file.

Check current requirements and figures with a qualified adviser — forms, thresholds, and penalties change, and this file is a signpost, not a source.

## 8. Working the checklist

Turn the sections above into your own list in `founder/ops/ops-legal.md`, each item tagged **essential-now**, **soon**, or **waiting-on-trigger**, with an owner and a date. Revisit it at the quarterly reconciliation. Two habits keep it from rotting: (1) when something becomes real (a first paying customer, a first EU user, a first contractor), pull the matching item forward; (2) whenever an item needs a professional, book the conversation rather than guessing.

---

*Reference and first-draft material only. Not legal, tax, or entity advice. Entity choice, filings, and document wording are the founder's decisions, made with a qualified professional where the stakes warrant.*
