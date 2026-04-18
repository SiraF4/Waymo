import random
import matplotlib.pyplot as plt

#  Attack parameters 
num_accounts         = 1000  # total Waymo user accounts
breach_db_size       = 500   # credentials attacker has from leaked database
attack_rate          = 50    # login attempts per second
password_reuse_rate  = 0.40  # 40% of users reuse leaked passwords
mfa_adoption_rate    = 0.20  # 20% of users have MFA enabled
rate_limit_threshold = 10    # failed attempts before IP is blocked

# System performance parameters 
normal_response_time    = 0.2   # seconds = normal app login response time
overload_delay_per_attempt = 0.005  # each attack attempt adds server delay
lockout_response_time   = 5.0   # seconds to recover a locked account

# building account database (for attackers assumptions) 
random.seed(42)
accounts = []
for i in range(num_accounts):
    accounts.append({
        "id":              i,
        "reused_password": random.random() < password_reuse_rate,
        "has_mfa":         random.random() < mfa_adoption_rate,
    })

# simulation function(s) 
def run_attack(accounts, rate_limiting=False, mfa_enabled=False):
    compromised_count    = []   # total compromised accounts over time
    response_times       = []   # system response time degradation
    locked_out_users     = []   # legitimate users locked out
    failed_attempts      = 0
    compromised_total    = 0
    locked_out_total     = 0

    for i, account in enumerate(accounts[:breach_db_size]):

        # Measure system response time degradation 
        current_response_time = normal_response_time + (i * overload_delay_per_attempt)
        response_times.append(current_response_time)

        # Rate limiting countermeasure 
        if rate_limiting and failed_attempts >= rate_limit_threshold:
            compromised_count.append(compromised_total)
            locked_out_users.append(locked_out_total)
            continue

        # Checking if account is vulnerable 
        vulnerable = account["reused_password"]
        protected  = account["has_mfa"] and mfa_enabled

        if vulnerable and not protected:
            compromised_total += 1  # attacker gains access

        else:
            failed_attempts += 1
            # legitimate user gets locked out after repeated failed attempts
            if failed_attempts % rate_limit_threshold == 0:
                locked_out_total += 1  # incorrect system action —-> wrong user locked out

        compromised_count.append(compromised_total)
        locked_out_users.append(locked_out_total)

    return compromised_count, response_times, locked_out_users

# Run Three Scenarios 
comp1, resp1, lock1 = run_attack(accounts, rate_limiting=False, mfa_enabled=False)
comp2, resp2, lock2 = run_attack(accounts, rate_limiting=True,  mfa_enabled=False)
comp3, resp3, lock3 = run_attack(accounts, rate_limiting=True,  mfa_enabled=True)

x = list(range(breach_db_size))


########################################################################################################################
########################################################################################################################
# Print Statements
print("=" * 45)
print("   Waymo Account Attack Simulation Summary")
print("=" * 45)
print(f"{'Scenario':<25} {'Compromised':>12} {'Locked Out':>12}")
print("-" * 45)
print(f"{'No Defense':<25} {comp1[-1]:>12} {lock1[-1]:>12}")
print(f"{'Rate Limiting Only':<25} {comp2[-1]:>12} {lock2[-1]:>12}")
print(f"{'Rate Limit + MFA':<25} {comp3[-1]:>12} {lock3[-1]:>12}")
print("=" * 45)
print(f"\nSystem Response Time (no defense):")
print(f"  Start : {resp1[0]:.3f}s")
print(f"  End   : {resp1[-1]:.3f}s  <-- degraded performance")

########################################################################################################################
########################################################################################################################
# Plot (3 in one to "collage" the results)
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Waymo Credential Stuffing Attack — System Impact", fontsize=14)

# Plot 1: Accounts Compromised
axes[0].plot(x, comp1, color="red",    label="No Defense")
axes[0].plot(x, comp2, color="orange", label="Rate Limiting")
axes[0].plot(x, comp3, color="green",  label="Rate Limit + MFA")
axes[0].set_title("Accounts Compromised Over Time")
axes[0].set_xlabel("Login Attempts")
axes[0].set_ylabel("Compromised Accounts")
axes[0].legend()
axes[0].grid(True)

# Plot 2: System Response Time Degradation
axes[1].plot(x, resp1, color="red",    label="No Defense")
axes[1].plot(x, resp2, color="orange", label="Rate Limiting")
axes[1].plot(x, resp3, color="green",  label="Rate Limit + MFA")
axes[1].set_title("System Response Time Degradation")
axes[1].set_xlabel("Login Attempts")
axes[1].set_ylabel("Response Time (seconds)")
axes[1].legend()
axes[1].grid(True)

# Plot 3: Legitimate Users Locked Out (Incorrect System Action)
axes[2].plot(x, lock1, color="red",    label="No Defense")
axes[2].plot(x, lock2, color="orange", label="Rate Limiting")
axes[2].plot(x, lock3, color="green",  label="Rate Limit + MFA")
axes[2].set_title("Legitimate Users Locked Out")
axes[2].set_xlabel("Login Attempts")
axes[2].set_ylabel("Locked Out Users")
axes[2].legend()
axes[2].grid(True)

plt.tight_layout()
plt.show()