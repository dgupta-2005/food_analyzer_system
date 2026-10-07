from typing import List
from datetime import datetime
from app.schemas.user import UserProfileResponse
from app.schemas.meal import MealLogResponse
from app.schemas.recommendation import MealPlanResponse, DailyMealSlot, RecommendedDish
from app.schemas.product import ProductNutritionSchema

class RecommendationService:
    def generate_personalized_plan(
        self, profile: UserProfileResponse, recent_logs: List[MealLogResponse]
    ) -> MealPlanResponse:
        """Generates adaptive diet/meal plan based on user macro goals and past eating habits."""
        target_calories = profile.target_daily_calories
        goal = profile.primary_goal

        # Calculate average logged calories over recent logs
        if recent_logs:
            avg_calories = sum(log.total_calories for log in recent_logs) / len(recent_logs)
            avg_protein = sum(log.total_protein_g for log in recent_logs) / len(recent_logs)
        else:
            avg_calories = target_calories
            avg_protein = profile.target_protein_g

        # Determine macro distribution per meal slot
        breakfast_cal = round(target_calories * 0.25)
        lunch_cal = round(target_calories * 0.35)
        snack_cal = round(target_calories * 0.15)
        dinner_cal = round(target_calories * 0.25)

        slots = [
            DailyMealSlot(
                slot_name="Breakfast",
                target_calories=breakfast_cal,
                recommended_dishes=[
                    RecommendedDish(
                        dish_name="Oatmeal with Almond Milk, Chia Seeds & Berries",
                        portion_size="1 bowl (250g)",
                        target_calories=breakfast_cal,
                        protein_g=14.0,
                        carbs_g=45.0,
                        fats_g=8.0,
                        reason="High fiber, low glycemic index, sustained morning energy."
                    )
                ]
            ),
            DailyMealSlot(
                slot_name="Lunch",
                target_calories=lunch_cal,
                recommended_dishes=[
                    RecommendedDish(
                        dish_name="Grilled Paneer/Chicken Salad with Multigrain Roti & Dal",
                        portion_size="1 balanced plate",
                        target_calories=lunch_cal,
                        protein_g=35.0,
                        carbs_g=55.0,
                        fats_g=15.0,
                        reason="High protein meal to support recovery and preserve lean muscle mass."
                    )
                ]
            ),
            DailyMealSlot(
                slot_name="Evening Snack",
                target_calories=snack_cal,
                recommended_dishes=[
                    RecommendedDish(
                        dish_name="Roasted Makhana (Fox Nuts) & Green Tea",
                        portion_size="1 cup (40g)",
                        target_calories=snack_cal,
                        protein_g=6.0,
                        carbs_g=22.0,
                        fats_g=3.0,
                        reason="Crunchy low-calorie snack replacing deep-fried chips."
                    )
                ]
            ),
            DailyMealSlot(
                slot_name="Dinner",
                target_calories=dinner_cal,
                recommended_dishes=[
                    RecommendedDish(
                        dish_name="Steamed Tofu/Fish Curry with Brown Rice & Stir-fried Veggies",
                        portion_size="1 bowl",
                        target_calories=dinner_cal,
                        protein_g=28.0,
                        carbs_g=40.0,
                        fats_g=10.0,
                        reason="Light, easily digestible meal suited for evening metabolism."
                    )
                ]
            )
        ]

        advice = (
            f"Based on your profile goal ({goal.upper()}) and daily target of {target_calories} kcal: "
            f"Your historical average intake was ~{round(avg_calories)} kcal/day. "
            f"Ensure you consume at least {profile.target_protein_g}g of protein daily."
        )

        return MealPlanResponse(
            plan_title=f"Customized {goal.capitalize()} Nutrition Strategy",
            target_daily_calories=target_calories,
            user_goal=goal,
            daily_slots=slots,
            overall_advice=advice,
            generated_at=datetime.utcnow()
        )

recommendation_service = RecommendationService()
