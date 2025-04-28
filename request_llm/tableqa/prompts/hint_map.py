# coding=utf-8
"""
author: 卓可秋
date:2025/4/26
修改：
功能：

"""

table_class_hint_map={
    'result table':"""What methods and their corresponding measurements are shown in the table?
1)  Start by listing each method presented in the table.
2)  For each method, please specify the corresponding metric values.
3)  Summarize the information in a structured manner.
Which method performs the best in each metric? Provide the specific values.
1)  Compare the metric values of each method.
2)  Identify the method that performs the best in each metric and provide the specific values.
3)  Summarize the findings.
Which method has the most balanced performance across all metrics? Explain your reasoning.
1)  Assess the balance of the results for each method.
2)  Identify the method with consistent performance across these metrics.
3)  Provide an explanation for why this method is considered the most balanced.
    """,
    'statistical table':"""What datasets and their corresponding statistical measures are shown in the table?
1)  Start by listing each dataset presented in the table.
2)  For each dataset, note the corresponding mean, median and standard deviation.
3)  Summarize the information in a structured manner.
Which dataset has the highest mean, and what is the value?
1)  Compare the mean values of each dataset.
2)  Identify the dataset with the highest mean and provide the specific value.
3)  Summarize the findings.
What considerations should be considered when interpreting these statistical results?
1)  Identify potential limitations of the statistical analysis.
2)  Discuss considerations such as sample size, data distribution, and outliers.
3)  Summarize the impact of these limitations on the results.
    """,
    'method comparison table': """What are the methods being compared and their corresponding performance metrics?
1)  List each method presented in the table.
2)  Note the corresponding metric values for each method.
3)  Summarize the information.
Which method exhibits the highest overall performance across all metrics, and how is this determined?
1)  Compare the accuracy, precision, recall, and F1 score of each method.
2)  Determine the method that performs consistently well across all metrics.
3)  Summarize the findings and provide the reasoning.
If you were to recommend one method based on these results, which would it be and why?
1)  Review the performance of each method based on the provided metrics.
2)  Choose the method with the best overall performance and balance.
3)  Justify the recommendation based on the data.
    """,
    'configuration or parameter table': """How many parameters are listed in the table, and what are they?
1)  Count the number of parameters listed in the table.
2)  List each parameter.
3)  Summarize the findings.
What are the parameter values for each method shown in the table?
1)  List each parameter presented in the table.
2)  Note the corresponding values for different Method.
3)  Summarize the information.
Why is it important to document the configuration and parameter settings in an experiment?
1)  Explain the role of configuration and parameter settings in experiments.
2)  Discuss the importance of reproducibility and consistency.
3)  Summarize the significance of documenting these settings.
What considerations should be considered when interpreting the parameter settings in this table?
1)  Identify potential limitations or factors influencing the parameter choices.
2)  Discuss considerations such as the specific application, data characteristics, and experimental goals.
3)  Summarize how these considerations affect the interpretation of the parameter settings.
    """,
    'summary or review table': """How many studies are summarized in the table, and what are their names?
1)  Count the number of studies listed in the table.
2)  List the names of each study.
3)  Summarize the findings.
What are the main findings of each study?
1)  List each study presented in the table.
2)  Note the corresponding main findings for each study.
3)  Summarize the information.
How do the methodologies differ among the studies, and what might be the reason for these differences?
1)  List the methodologies used in each study.
2)  Identify the differences in methodologies.
3)  Discuss possible reasons for these methodological differences in the context of the studies.
Why is it important to provide a summary or review table in a scientific paper?
1)  Explain the role of summary or review tables in scientific papers.
2)  Discuss the importance of providing a comprehensive overview and comparison.
3)  Summarize the significance of such tables for readers.
    """,
    'timeline and schedule table': """What are the start and end dates for each phase or task?
1)  List each phase or task presented in the table.
2)  Note the corresponding start and end dates for each phase or task.
3)  Summarize the information.
How does the timeline ensure that the project stays on track?
1)  Explain the role of start and end dates in managing the project timeline.
2)  Discuss how milestones help in tracking progress and ensuring timely completion.
3)  Summarize the importance of a well-defined timeline.
Why is it important to document the timeline and schedule in a research project?
1)  Explain the role of timeline and schedule documentation in research projects.
2)  Discuss the importance of planning, tracking progress, and ensuring deadlines are met.
3)  Summarize the significance of documenting these details.
    """,
    'other types of table':"""What are the key metrics presented in the table, and what do they represent?
1)Identify the metrics listed in the table.
2)Describe what each metric represents in the context of the study.
3)Summarize the significance of these metrics for the overall findings.
How do the values of the key metrics vary across different categories or groups in the table?
1)List the categories or groups presented in the table.
2)Compare the values of key metrics across these categories or groups.
3)Highlight any significant differences or trends.
How can the findings presented in the table be applied in practical scenarios?
1)Summarize the key findings from the table.
2)Discuss potential practical applications of these findings.
3)Provide examples of how these findings can be implemented in real-world scenarios.
How does the data in the table support or contradict the hypotheses or objectives of the study?
1)State the hypotheses or objectives of the study.
2)Compare the data in the table with these hypotheses or objectives.
Discuss whether the data supports or contradicts them and why.
    """
}


