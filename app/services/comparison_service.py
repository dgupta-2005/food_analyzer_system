from typing import List, Tuple
from app.schemas.product import ProductNutritionSchema, StatisticalComparisonSchema

SCORE_MAP = {"A": 5.0, "B": 4.0, "C": 3.0, "D": 2.0, "E": 1.0}

class HealthComparisonEngine:
    def calculate_statistical_metrics(
        self, original: ProductNutritionSchema, alternative: ProductNutritionSchema
    ) -> StatisticalComparisonSchema:
        """Calculates quantitative statistical measures and deltas between two food products."""
        # 1. Calorie Reduction Percentage
        orig_cal = max(1.0, original.calories_100g)
        cal_reduction_pct = round(((orig_cal - alternative.calories_100g) / orig_cal) * 100.0, 1)

        # 2. Sugar Reduction Percentage
        orig_sugar = max(0.1, original.sugar_100g)
        sugar_reduction_pct = round(((orig_sugar - alternative.sugar_100g) / orig_sugar) * 100.0, 1)

        # 3. Protein Increase Percentage
        orig_protein = max(0.1, original.protein_100g)
        protein_increase_pct = round(((alternative.protein_100g - orig_protein) / orig_protein) * 100.0, 1)

        # 4. Composite Health Score Delta
        orig_score = SCORE_MAP.get((original.nutri_score or "C").upper(), 3.0)
        alt_score = SCORE_MAP.get((alternative.nutri_score or "A").upper(), 5.0)
        score_delta = round(alt_score - orig_score, 1)

        # 5. Natural Language Verdict Synthesis
        verdict_parts = []
        if cal_reduction_pct > 0:
            verdict_parts.append(f"{cal_reduction_pct}% lower calories")
        if sugar_reduction_pct > 0:
            verdict_parts.append(f"{sugar_reduction_pct}% less sugar")
        if protein_increase_pct > 0:
            verdict_parts.append(f"{protein_increase_pct}% more protein per serving")

        verdict_text = f"{alternative.product_name} is a healthier alternative with " + (", ".join(verdict_parts) if verdict_parts else "better overall macro balance.")

        return StatisticalComparisonSchema(
            original_product=original,
            alternative_product=alternative,
            calorie_reduction_pct=cal_reduction_pct,
            sugar_reduction_pct=sugar_reduction_pct,
            protein_increase_pct=protein_increase_pct,
            health_score_delta=score_delta,
            summary_verdict=verdict_text
        )

comparison_engine = HealthComparisonEngine()
