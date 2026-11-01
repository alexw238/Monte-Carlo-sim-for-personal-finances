import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import functions.Monte_Carlo as MC

# Define our start conditions
Config = {
    "iterate": 1000, # number of iterations for the monte carlo simulation
    
    # Sets up our balance params
    "init_balance": 2000,
    "min_balance": 100,
    "max_bal": 500,

    # Sets up ISA related params
    "ISA": 10000,
    "LISA": 0,
    "Ann_LISA_add": 4000,
    "prop_gov_LISA_add": 0.25,
    "mean_ann_stmkt_return": 0.1,
    "sd_ann_stmkt_return": 0.13,

    # Sets up savings account params
    "savings": 1000,
    "min_save": 500,
    "apr": 0.05,

    # Sets up income params
    "mean_weekly_income": 200,
    "sd_weekly_income": 15,

    # Sets up loan params
    "year_loan": 5000,
    "fee_loan": 9500,
    "loan_interest": 0.05,

    # Sets up weekly spending params
    "mean_weekly_spend": 200,
    "sd_weekly_spend": 30,

    # Defines our annual rent
    "annual_rent": 10500,

    # Sets number of weeks to simulate
    "no_weeks": 156,

    #Placement year params (don't touch "Placement year": False)
    "Placement year": False,
    "Placement year Start week": 52,
    "Placement year Salary": 25000,
    "Placement year Fee loan": 3400,
}

##############################################################################
# main - time unit is weeks                                                  #
##############################################################################

# Set the random seed 
np.random.seed(28907314)

# run the monte carlo simulation for placement year/ no placement year
sims, mean_vector, interval_95, loan_val = MC.MonteCarlo(Config)

Config["Placement year"] = True

sims_2, mean_vector_2, interval_95_2, loan_val_2 = MC.MonteCarlo(Config)

# print the total loan value at the end of the simulation
print(f"loan value (no Placement) at week" 
      f"{Config['no_weeks']}: {loan_val[-1][0]}"
      )

print(f"loan value (Placement) at week" 
      f"{Config['no_weeks']}: {loan_val_2[-1][0]}"
      )


# Plotting graphs
fig1 = plt.figure(figsize=(10, 8))  # makes figure with size 10 by 8 inches

# Set up the grid for the subplots making row 1 smaller than row 2
gs = gridspec.GridSpec(2, 2, height_ratios=[5, 7])

# Add subplots to the grid in our figure
ax1 = fig1.add_subplot(gs[0, 0])
ax2 = fig1.add_subplot(gs[0, 1])
ax3 = fig1.add_subplot(gs[1, :]) # makes a big 3rd plot on bottom row

ax1.set_title("Plot of total balance with time no Placement")

ax1.set_xlim(0, Config["no_weeks"])

# Plot the 95% confidence interval and mean for the first simulation
ax1.fill_between(np.arange(1, Config["no_weeks"]), 
                 interval_95[0, 1:],
                 interval_95[1, 1:], 
                 alpha=0.3,
                 color = "blue"
                 )
# Plot the mean for the first simulation
ax1.plot(np.arange(1, Config["no_weeks"]),
          mean_vector[1:],
          color = "navy"
         )

ax1.set_xlabel("Weeks")
ax1.set_ylabel("Total balance (£)")
ax1.legend(["95%" " confidence interval", "Mean"])


ax2.set_title("Plot of total balance with time Placement")

ax2.set_xlim(0, Config["no_weeks"])

# Plot the 95% confidence interval and mean for the second simulation
ax2.fill_between(np.arange(1, Config["no_weeks"]), 
                 interval_95_2[0, 1:],
                 interval_95_2[1, 1:], 
                 alpha=0.3,
                 color = "orange"
                 )
# Plot the mean for the second simulation
ax2.plot(np.arange(1, Config["no_weeks"]), 
         mean_vector_2[1:],
         color = "darkorange"
         )

ax2.set_xlabel("Weeks")
ax2.set_ylabel("Total balance (£)")
ax2.legend(["95%" " confidence interval", "Mean"])


ax3.set_title("Plot of total balance with time Placement and no Placement")

ax3.set_xlim(0, Config["no_weeks"])

#plot the 95% confidence interval and mean for both simulations on same graph
ax3.fill_between(np.arange(1, Config["no_weeks"]), 
                 interval_95[0, 1:],
                 interval_95[1, 1:], 
                 alpha=0.3,
                 color = "blue"
                 )
ax3.fill_between(np.arange(1, Config["no_weeks"]), 
                 interval_95_2[0, 1:],
                 interval_95_2[1, 1:], 
                 alpha=0.3,
                 color = "orange"
                 )

line1 =ax3.plot(np.arange(1, Config["no_weeks"]),
          mean_vector[1:],
          color = "navy"
         )
line2 = ax3.plot(np.arange(1, Config["no_weeks"]), 
         mean_vector_2[1:],
         color = "darkorange"
         )

ax3.set_xlabel("Weeks")
ax3.set_ylabel("Total balance (£)")
ax3.legend([line1[0], line2[0]], ["No Placement", "Placement"])

fig1.tight_layout()
plt.show()