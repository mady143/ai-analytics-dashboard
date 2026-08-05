"""
Builder NLP — Universal NLP Intent Classifier & Typo Normalizer for Builder Agent.
Keeps agents/builder_agent.py lightweight (< 250 lines).
"""

def classify_task_intent_and_intent_map(task_title: str, description: str) -> dict:
    """
    Universal NLP Intent Classifier & Typo Normalizer.
    Parses natural language statements, typos, and screenshot descriptions
    to map them to concrete feature domains & action specs.
    """
    text_clean = f"{task_title} {description}".lower().replace("-", " ").replace("_", " ").replace(".", " ").replace(",", " ")
    
    intents = []
    actions = []

    # 1. Pagination & Total Records (handles typos: fecth, pagenation, page, records, total, rows, limit, offset, count)
    pagination_keywords = ["pagenation", "pagination", "page", "paging", "paginate", "fecth", "fetch", "total records", "record count", "row count", "rows", "items count", "total count"]
    if any(k in text_clean for k in pagination_keywords):
        intents.append("PAGINATION_AND_TOTAL_RECORDS")
        actions.append("ENFORCE_TABLE_PAGINATION_CONTROLS_AND_TOTAL_RECORDS_DISPLAY")

    # 2. Date Parameter & Header Filtering (handles: date, oerdte, order date, calendar, time, header, datepicker, day)
    date_keywords = ["date", "oerdte", "order date", "calendar", "header date", "datepicker", "day", "time"]
    if any(k in text_clean for k in date_keywords):
        intents.append("DATE_PARAMETER_FILTERING")
        actions.append("ENFORCE_STRICT_HEADER_DATE_PARAMETER_PROPAGATION")

    # 3. AI Copilot Search & Date-Agnostic Querying (handles: copilot, ai, ask ai, nlp, query, prompt, search)
    copilot_keywords = ["copilot", "ai copilot", "ask ai", "nlp", "search", "prompt", "natural language"]
    if any(k in text_clean for k in copilot_keywords):
        intents.append("AI_COPILOT_DATE_AGNOSTIC_QUERY")
        actions.append("ENFORCE_COPILOT_FULL_DATASET_SEARCH_WITHOUT_DATE_FILTER")

    # 4. Scratch Quantity & Critical Anomaly Alerts (handles: scratch, scrtch, missing, anomaly, risk, alert)
    scratch_keywords = ["scratch", "scrtch", "missing", "anomaly", "risk", "alert", "critical"]
    if any(k in text_clean for k in scratch_keywords):
        intents.append("SCRATCH_QUANTITY_ANOMALY_ALERTS")
        actions.append("ENFORCE_RED_CRITICAL_SCRATCH_ANOMALY_LOGIC")

    # 5. Charts & Visualizations (handles: chart, graph, bar, scatter, plot, heatmap, visualization, ticks)
    chart_keywords = ["chart", "graph", "bar", "scatter", "plot", "heatmap", "visualization", "ticks"]
    if any(k in text_clean for k in chart_keywords):
        intents.append("CHARTS_AND_VISUALIZATION_ALIGNMENT")
        actions.append("ALIGN_CHART_TICKS_AND_KPI_WAREHOUSE_COUNT")

    # 6. Navbar & Navigation (handles: nav, navbar, menu, sidebar, header)
    nav_keywords = ["nav", "navbar", "navigation", "menu", "sidebar", "header controls"]
    if any(k in text_clean for k in nav_keywords):
        intents.append("NAVBAR_AND_SIDEBAR_NAVIGATION")
        actions.append("BUILD_OR_UPDATE_NAVBAR_SIDEBAR_COMPONENTS")

    # 7. Multi-Target Database Architecture (handles: database, target db, postgres, oracle, db switch)
    db_keywords = ["database", "target db", "postgres", "oracle", "db switch"]
    if any(k in text_clean for k in db_keywords):
        intents.append("MULTI_TARGET_DATABASE_ARCHITECTURE")
        actions.append("ENFORCE_MULTI_TARGET_DATABASE_CONFIGURATIONS")

    # 8. Dynamic NLP Intent Extractor (Fallback for ANY arbitrary user request, statement, or screenshot note)
    if not intents:
        raw_words = [w for w in text_clean.split() if len(w) > 3 and w not in ["the", "this", "that", "from", "with", "have", "need", "please", "make", "will", "your"]]
        intent_tag = f"DYNAMIC_FEATURE_INTENT_{'_'.join([w.upper() for w in raw_words[:3]])}" if raw_words else "GENERAL_DASHBOARD_ENHANCEMENT"
        intents.append(intent_tag)
        actions.append(f"EXECUTE_DYNAMIC_LLM_CODE_GENERATION_FOR_{intent_tag}")

    return {
        "intents": intents,
        "actions": actions
    }
