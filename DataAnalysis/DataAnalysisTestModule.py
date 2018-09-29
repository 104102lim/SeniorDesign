# -*- coding: utf-8 -*-
"""
    -----------------------------------------------------------------------
    DataAnalysisTestModule.py
    : Test Module for Data Analysis Module of BH Oil Characterization Software Applcation
    Author: Sungho Lim, Joey Gallardo
    09/28/2018
    -----------------------------------------------------------------------
    """


#-----------------------------------------------------------------------
# 0. NECESSARY LIBRARY
#-----------------------------------------------------------------------

import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import struct



