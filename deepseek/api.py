from openai import OpenAI

# Please install OpenAI SDK first: `pip3 install openai -i https://pypi.tuna.tsinghua.edu.cn/simple`

client = OpenAI(api_key="sk-d0a0e5d5358e4d579ac8c5afc2961c37", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你好，现在你是一名人类学、社会学方面的专家，擅长将人类学和社会学方面的图书从英文译成中文。今天我们翻译人类学学者Tim Ingold 和 Jo Lee Vergunst编辑的作品Ways of Walking Ethnography and Practice on Foot这本书，中文名字是《行走之道：步行中的民族志与实践》，具体规则如下： - 翻译时要准确传达原文的事实和背景。 - 即使上意译也要保留原始段落格式，以及保留人类学或者社会学术语。保留公司和博物馆缩写等。 - 人名要翻译，中文人名后加括号，括号里写清楚英文原名。 - 同时要保留引用的论文，例如 20 这样的引用。 - 在翻译专业术语时，第一次出现时要在括号里面写上英文原文，之后就可以只写中文了。 策略：分三步进行翻译工作，并打印每步的结果： 1. 根据英文内容直译，保持原有格式，不要遗漏任何信息 2. 根据第一步直译的结果，指出其中存在的具体问题，要准确描述，不宜笼统的表示，也不需要增加原文不存在的内容或格式，包括不仅限于： - 不符合中文表达习惯，明确指出不符合的地方 - 语句不通顺，指出位置，不需要给出修改意见，意译时修复 - 晦涩难懂，不易理解，可以尝试给出解释 3. 根据第一步直译的结果和第二步指出的问题，重新进行意译，保证内容的原意的基础上，使其更易于理解，更符合中文的表达习惯，同时保持原有的格式不变，除术语和专业表达以外，其余表述要求简单、清楚，不要过多有文学色彩的表达。"},
        {"role": "user", "content": "The books in this series explore the relations, in human social and cultural life, between perception, creativity and skill. Their common aim is to move beyond established approaches in anthropology and material culture studies that treat the inhabited world as a repository of complete objects, already present and available for analysis. Instead, these works focus on the creative processes that continually bring these objects into being, along with the persons in whose lives they are entangled."},
    ],
    stream=False
)

print(response.choices[0].message.content)