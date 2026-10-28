# styling for header
def headerStyle(header):
    return f"""
        <div style='
            font-size:2.2rem;
            font-weight: bold;
            font-family: cursive;
            color: #fff000;
            border: 1px solid #000fff;
            padding: 5px 10px;
            text-align:center;
            margin: 20px 0;
        '>
            {header}
        </div>
    """
        
        
        
# Styling for KPIs
def kpiStyle(label:str, value:str):
    return f"""
        <div style='text-align: center; border-left:3px solid #fff000;
            border-bottom-left-radius:10px; border-top-left-radius:10px;'>
            <div style='font-size: 1.4rem; margin: 10px 0'>
                {label}
            </div>
            <div>
                {value}
            </div>
        </div>

    """
