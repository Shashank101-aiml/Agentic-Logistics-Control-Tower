from backend.weather import get_weather_risk

def run_pipeline(city):
    # Step 1: Get weather data
    weather_data = get_weather_risk(city)

    # Step 2: Extract risk
    risk_score = weather_data["risk_score"]

    # Step 3: Decision logic
    if risk_score < 30:
        status = "SAFE"
    elif risk_score < 70:
        status = "WARNING"
    else:
        status = "HIGH RISK"

    return {
        "city": city,
        "risk_score": risk_score,
        "status": status,
        "details": weather_data
    }


# 🔥 TEST BLOCK (must be at bottom)
if __name__ == "__main__":
    cities = ["London", "Singapore", "Dubai"]
    for city in cities:
        result = run_pipeline(city)
        print(result)