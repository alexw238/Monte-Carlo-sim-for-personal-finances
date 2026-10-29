import numpy as np
from Classes.FEQ import FEQ 

# Define our start conditions

iterate = 10000

# Cash inflow
ISA = 10000
LISA = 0
Ann_LISA_add = 4000
prop_gov_LISA_add = 0.25
savings = 2000
apr = 0.05
weekly_income = 80
year_loan = 5000
mean_ann_stmkt_return = 0.1
sd_ann_stmkt_return = 0.13
init_balance = 2000

# Cash outflow
fee_loan = 9500
mean_weekly_spend = 200
sd_weekly_spend = 8
annual_rent = 10500
loan_interest = 0.05

no_weeks = 156 # Number of weeks to simulate

##############################################################################
# main - time unit is weeks                                                  #
##############################################################################

np.random.seed(28907314)

# Creates list for all the outputs of the monte carlo sim
potential_money = []

for i in range(iterate):

    # Sets up initial future events queue to be added to
    feq_i = FEQ([[ISA +
                 LISA +
                 savings +
                 init_balance, 0]])

    # Sets up all the lists of event's in the right format
    week_spends = [[0, 0]]
    week_in = [[0, 0]]
    ISA_changes = [[ISA, 0]]
    ISA_value = [0]
    LISA_changes = [[LISA, 0]]
    LISA_value = [0]
    rent_bills = [[0, 0]]
    saved_money = [[0, 0]]
    loan_take_out = [[0, 0]] # Money in from taking out a loan
    loan_fees = [[0, 0]]

    for j in range(1, no_weeks + 1):

        # Calculates weekly in and outflow and makes an event for it
        week_spends.append([((-1) * np.random.normal(mean_weekly_spend,
                                            (sd_weekly_spend ** 2)
                                            )),
                                            j]
                                            )
        
        week_in.append([weekly_income, j])

    for j in range(13, no_weeks + 1, 13):

        # Calculates everything that is factored in quarterly and makes an
        # Event for each quarter
        ISA_value.append(ISA_value[-1] + ISA_changes[-1][0])

        ISA_changes.append([(np.random.normal(mean_ann_stmkt_return,
                                            (sd_ann_stmkt_return ** 2) /
                            4)) *
                            ISA_value[-1],
                            j]
                            )

        LISA_value.append(LISA_value[-1] + LISA_changes[-1][0])
        
        LISA_changes.append([(prop_gov_LISA_add + 
                                np.random.normal(mean_ann_stmkt_return,
                                            (sd_ann_stmkt_return ** 2)) /
                                4) *
                            LISA_value[-1] +
                            Ann_LISA_add / 4,
                            j]
                            )

        rent_bills.append([(-1) * annual_rent / 4, j])

        saved_money.append([savings * (1 + (apr / 4)), j])

        loan_take_out.append([year_loan / 4, j])

    for j in range(52, no_weeks + 1, 52):

        # Calculates loan_fees yearly and makes an event for each year
        loan_fees.append([(-1) *
                         (1 + loan_interest) *
                         ((-1)*
                          loan_fees[-1][0] +
                          fee_loan +
                          year_loan),
                          j])
    # Adds all the events we just created to our queue
    feq_i = feq_i.add_list(week_spends)
    feq_i = feq_i.add_list(saved_money)
    feq_i = feq_i.add_list(week_in)
    feq_i = feq_i.add_list(ISA_changes)
    feq_i = feq_i.add_list(LISA_changes)
    feq_i = feq_i.add_list(rent_bills)
    feq_i = feq_i.add_list(loan_take_out)
    feq_i = feq_i.add_list(loan_fees)

    # Gets initial value for total money
    money = feq_i.FEQ[0][0]

    # Calculates money after each event happens leaving a final total
    for event in feq_i.FEQ:
        money = money + feq_i.FEQ[0][0]
        feq_i = feq_i.GoToNext()[0]
    
    potential_money.append(money)

print(max(potential_money), min(potential_money), np.mean(potential_money), potential_money)




