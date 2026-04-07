import random
import matplotlib.pyplot as plt

# ── Parameters ──────────────────────────────────────────────
num_accounts        = 1000   # total Waymo user accounts
attack_rate         = 50     # login attempts per second
password_reuse_rate = 0.40   # 40% of users reuse leaked passwords
mfa_adoption_rate   = 0.20   # 20% of users have MFA enabled
rate_limit_threshold= 10     # failed attempts before IP is blocked
breach_db_size      = 500    # number of leaked credentials attacker has

# ── Build account database ───────────────────────────────────
accounts = []
for i in range(num_accounts):
    accounts.append({
        "id":             i,
        "reused_password": random.random() < password_reuse_rate,
        "has_mfa":         random.random() < mfa_adoption_rate,
    })

# ── Simulation function ──────────────────────────────────────
def run_attack(accounts, rate_limiting=False, mfa_enabled=False):
    compromised   = []
    total_attempts= 0
    blocked       = 0
    failed_attempts = 0

    for account in accounts[:breach_db_size]:   # attacker only has breach_db_size credentials
        total_attempts += 1

        # Rate limiting countermeasure
        if rate_limiting and failed_attempts >= rate_limit_threshold:
            blocked += 1
            continue

        # Check if account is vulnerable
        vulnerable = account["reused_password"]
        protected  = account["has_mfa"] and mfa_enabled

        if vulnerable and not protected:
            compromised.append(total_attempts)  # log when it was compromised
        else:
            failed_attempts += 1

    return compromised, total_attempts, blocked

# ── Run three scenarios ──────────────────────────────────────
comp_no_defense,   total1, _ = run_attack(accounts, rate_limiting=False, mfa_enabled=False)
comp_rate_limit,   total2, b = run_attack(accounts, rate_limiting=True,  mfa_enabled=False)
comp_full_defense, total3, _ = run_attack(accounts, rate_limiting=True,  mfa_enabled=True)

# ── Convert to cumulative counts over attempts ───────────────
def cumulative(events, total):
    curve = [0] * total
    for e in events:
        if e < total:
            curve[e] = 1
    # running sum
    for i in range(1, total):
        curve[i] += curve[i - 1]
    return curve

x = list(range(total1))
y1 = cumulative(comp_no_defense,   total1)
y2 = cumulative(comp_rate_limit,   total1)
y3 = cumulative(comp_full_defense, total1)

# ── Print summary ────────────────────────────────────────────
print("=== Waymo Account Attack Simulation ===")
print(f"Accounts targeted:            {breach_db_size}")
print(f"No defense   — compromised:   {len(comp_no_defense)}")
print(f"Rate limiting — compromised:  {len(comp_rate_limit)}  | blocked: {b}")
print(f"Rate limit + MFA — compromised: {len(comp_full_defense)}")

# ── Plot ─────────────────────────────────────────────────────
plt.figure(figsize=(10, 5))
plt.plot(x, y1, label="No Defense",          color="red")
plt.plot(x, y2, label="Rate Limiting Only",  color="orange")
plt.plot(x, y3, label="Rate Limit + MFA",    color="green")

plt.xlabel("Login Attempts")
plt.ylabel("Accounts Compromised")
plt.title("Waymo Credential Stuffing Attack Simulation")
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()