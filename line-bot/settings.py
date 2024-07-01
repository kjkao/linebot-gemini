from google.generativeai.types import HarmCategory, HarmBlockThreshold

safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

chatcfg = {
    "temperature": 1.0,
    "system_instruction": "如果對話內容是中文，使用繁體中文回應。",
}

transcfg = {
    "temperature": 0.3,
    "system_instruction": "你是語言翻譯專家，把對話內容，英文翻成繁體中文，中文翻成英文。直接提供翻譯，不再進行對話。",
}

teachcfg = {
    "temperature": 0.7,
    "system_instruction": "你是一個教導外國人英文的英文教師，可以在對話一開始詢問一些基本資訊(name, age, come from)。\n尋找話題來引導英文對話。提示對方對話回覆時可使用的片語，單字，和例句，如果對話中，有使用錯誤的語法或時態，或是有拼錯的字，都可以在對話中指正。\n\n格式如下:\n對話內容\n\n提示內容\n\n指正內容\n",
}
