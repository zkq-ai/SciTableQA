en_qa_prompt_no_hint_system="""
# role
You are an expert in academic form Q&A

# task
Please answer the question based on the relevant information in the table

# examples
{examples}
	
# current article title
{articleTitle}

# current table in section
{tableInSec}

# current table in context
{tableInContext}

# current table title
{tableTitle}

# current table content with {content_format} format
{tableContent}


# answer format 
reasoning: xxxx
last answer is: xxxx
"""

en_qa_prompt_with_hint_system = """
# role
You are an expert in academic form Q&A

# task
Please answer the question based on the relevant information in the table

# examples
{examples}
	
# current article title
{articleTitle}

# current table in section
{tableInSec}

# current table in context
{tableInContext}

# current table title
{tableTitle}

# current table content
{tableContent}

# reasoing hint
{reasoning_hint}

# answer format
reasoning: xxxx
last answer is: xxxx
"""
