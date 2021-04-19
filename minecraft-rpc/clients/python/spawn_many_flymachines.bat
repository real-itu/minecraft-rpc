for /L %%A IN (1000, 25, 2500) DO (
    CALL py stresstest_flyingmachines.py 1 %%A
)