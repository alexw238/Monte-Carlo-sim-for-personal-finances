import numpy as np
from Classes.FEQ import FEQ 

# Define our start conditions

iterate = 1

# Model Conditions
min_save = 500
min_balance = 100

# Cash inflow in £s
ISA = 10000    # Initial value for ISA
LISA = 0    # Initial value for lifetime ISA
Ann_LISA_add = 4000    # Annual addition to the lifetime ISA
prop_gov_LISA_add = 0.25
savings = 1000    # Value of savings account
apr = 0.05    # apr of said savings account
weekly_income = 130
year_loan = 5000    # yearly maintanence loan
mean_ann_stmkt_return = 0.1
sd_ann_stmkt_return = 0.13
init_balance = 2000    # Initial current account balance

# Cash outflow in £s
fee_loan = 9500    # Student fee loan
mean_weekly_spend = 800
sd_weekly_spend = 10
annual_rent = 10500    # Cost of annual rent
loan_interest = 0.05    # Interest on student loans

no_weeks = 156 # Number of weeks to simulate

##############################################################################
# main - time unit is weeks                                                  #
##############################################################################

np.random.seed(28907314)

# Creates list for all the outputs of the monte carlo sim
potential_ISA = []
potential_LISA = []
potential_bal = []
potential_sav = []
potential_total = []

# Finds final value of the loan
loan_val = [[0, 0]]

for j in range(52, no_weeks + 1, 52):
    loan_val.append([
        np.round(
            loan_val[-1][0] - 
            (
                ((-1) *
                loan_interest * 
                loan_val[-1][0]
            ) +
            fee_loan +
            year_loan
            ), 
        2),
    j
    ])

for i in range(iterate):

    # Sets up all the initial states of the simulation
    balance = [[init_balance, 0]]
    ISA_value = [[ISA, 0]]
    LISA_value = [[LISA, 0]]   
    rent_bills = [[0, 0]]
    saved_money = [[savings, 0]]

    for j in range(1, no_weeks + 1):
        ######################################################################
        # Calculates weekly in and outflow and makes events for them         #
        ######################################################################

        # Work out balance changes for week
        balance.append([
            (np.round(
                balance[-1][0] -
                np.random.normal(
                    mean_weekly_spend,
                    (sd_weekly_spend ** 2)
                ),
            2)
            ),
            j
        ])
                                            
        balance.append([
            np.round(
                balance[-1][0] + 
                weekly_income,
                2), 
            j
        ])

        if j in range(13, no_weeks + 1, 13):
            
            rent_bills.append([annual_rent / 4, j])
            balance.append([np.round(balance[-1][0] - rent_bills[-1][0], 2),
                             j])

            if j not in range(52, no_weeks + 1, 52):
                balance.append([np.round(balance[-1][0] + year_loan / 3, 2),
                                 j])

        # Account for taking money from savings
        if balance[-1][0] <= min_balance:
            take_from_sav = min_balance - balance[-1][0]
            saved_money.append([saved_money[-1][0] - take_from_sav, j])
            balance.append([(balance[-1][0] + take_from_sav), j])

        if saved_money[-1][0] <= min_save:
            take_from_ISA = min_save - saved_money[-1][0]
            ISA_value.append([ISA_value[-1][0] - take_from_ISA, j])
            saved_money.append([(saved_money[-1][0] + take_from_ISA), j])

        # ISA and savings both must not go negative
        if ISA_value[-1][0] <= 0:
            lost_money = 0 - ISA_value[-1][0]
            ISA_value.append([0, j])
            saved_money.append([saved_money[-1][0] - lost_money, j])

            if saved_money[-1][0] <= 0:
                lost_money = 0 - saved_money[-1][0]
                saved_money.append([0, j])
                balance.append([balance[-1][0] - lost_money, j])

        # Apply interest
        saved_money.append([np.round(saved_money[-1][0] * (1 + apr / 52), 2),
                            j])
        ISA_value.append([
            np.round(
                ISA_value[-1][0] *
                (
                1 + 
                np.random.normal(
                    mean_ann_stmkt_return, 
                    sd_ann_stmkt_return ** 2
                    ) / 52
                ),
            2),
            j
        ])

        if j in range(52, no_weeks + 1, 52):

            # Here I'll look at things that don't have balance changed weekly
            # and are effectively untouched in our time period 

            LISA_value.append([np.round(
                            (LISA_value[-1][0] +
                               Ann_LISA_add
                            ) *
                               (
                                1 +
                                prop_gov_LISA_add +
                                np.random.normal(mean_ann_stmkt_return,
                                                sd_ann_stmkt_return ** 2
                                            )
                               ),
                            2),
                        j
                    ])
    
    potential_ISA.append(ISA_value[-1])
    potential_LISA.append(LISA_value[-1])
    potential_bal.append(balance[-1])
    potential_sav.append(saved_money[-1])
    potential_total.append(sum([
        potential_ISA[-1][0],
        potential_LISA[-1][0],
        potential_bal[-1][0],
        potential_sav[-1][0],
    ]))


print(
    np.round(np.mean(potential_total), 2), 
    np.round(np.max(potential_total), 2), 
    np.round(np.min(potential_total), 2), 
    np.round(np.mean(potential_sav), 2), 
    np.round(np.mean(potential_LISA), 2), 
    np.round(np.mean(potential_ISA),2), 
    np.round(np.mean(potential_bal), 2), 
    loan_val[-1]
    )

