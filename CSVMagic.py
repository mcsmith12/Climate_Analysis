import pandas as pd
def csvfixer(main, replacement):
    """From Max and Thu: Enter the main and replacement in the following form('main.csv', 'replacement.csv')"""
    import pandas as pd
    main = pd.read_csv(main)
    replacement = pd.read_csv(replacement)
    
    row = main.query('actual_mean_temp == actual_min_temp').index
    for i in row:
        main.loc[i:i,'date':'record_precipitation'] = replacement.loc[i:i, 'date':'record_precipitation']
    
    return (main)

def csvMERGER(main, replacement):
    """This replaces the zero rows of main.csv with the rows from replacement.csv
    Note: the two csv's must be the same lengh, so as long as you scraped and parsed the same dates, you're fine.
    Further Note: rewriting the file creates an extra column named 'Unnamed: 0', this won't mess up the visualization.
    Example:
    main = 'KMIE.csv'
    replacement = 'KIND.csv'
    csvMERGER(main, replacement)"""
    
    import pandas as pd
    length = len(pd.read_csv(main))
    df = csvfixer(main, replacement).loc[0:length,'date':'record_precipitation']
    #This next step will produce an unnecessary column during the rewrite.
    #Don't worry about it. It doesn't change the visualizations.
    df.to_csv(main)