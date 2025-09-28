from manim import *
import numpy as np

# --- 1. Define Constants and Helper Function ---

# The original covariance matrix (e.g., sample covariance)
# 2x2 for simplicity: variance 1.0, covariance 0.8
SIGMA = np.array([
    [1.0, 0.8],
    [0.8, 1.0]
])

# The target matrix (e.g., identity or diagonal matrix)
# Variance 1.0, covariance 0.0 (fully uncorrelated)
TARGET = np.array([
    [1.0, 0.0],
    [0.0, 1.0]
])

def shrink_matrix(sigma, target, lambda_val):
    """
    Calculates the shrunk matrix: (1 - lambda) * sigma + lambda * target.
    Formats the output elements to strings with 2 decimal places.
    """
    # Calculate the shrunk matrix using linear combination
    shrunk = (1 - lambda_val) * sigma + lambda_val * target
    
    # Format all elements to strings with 2 decimal places (This fixes the precision issue)
    formatted_matrix = [[f"{x:.2f}" for x in row] for row in shrunk]
    
    return formatted_matrix

# --- 2. Manim Scene Class ---

class ShrinkageAnimation(Scene):
    def construct(self):
        # 1. Setup: ValueTracker for Lambda
        lambda_tracker = ValueTracker(0.0)

        # 2. Setup: Formula (The formula itself is static)
        formula = MathTex(
            r"\Sigma_{\lambda} = (1 - \lambda)", r"\Sigma", r" + ", r"\lambda", r"T",
            substrings_to_isolate=[r"\lambda", r"\Sigma", r"T"]
        ).scale(0.8).to_edge(UP, buff=1.0)
        
        # 3. Setup: Lambda Label (Uses always_redraw for clean updating and LaTeX rendering fix)
        # Fix: Using always_redraw and formatting the value ensures correct rendering
        lambda_label = always_redraw(
            lambda: MathTex(
                r"\lambda = " + f"{lambda_tracker.get_value():.2f}" # Combine into one string
            ).next_to(formula, DOWN, buff=0.5)
        )

        # 4. Setup: Matrix (The main object that will change)
        # The inner function is called whenever the tracker value changes
        shrinkage_matrix_mobj = always_redraw(
            lambda: Matrix(
                shrink_matrix(SIGMA, TARGET, lambda_tracker.get_value())
            ).next_to(formula, DOWN, buff=1.5)
        )
        
        # 5. Initial Display (lambda = 0)
        self.play(
            Write(formula),
            FadeIn(lambda_label), 
            FadeIn(shrinkage_matrix_mobj)
        )
        self.wait(1)

        # 6. Animate the Shrinkage (Lambda from 0.0 to 1.0)
        # Animate the tracker's value, which automatically updates the matrix and label
        self.play(
            lambda_tracker.animate.set_value(1.0),
            run_time=4,
            rate_func=linear
        )
        self.wait(1)
        
        # 7. Final Highlight (Highlight the off-diagonal zeros at lambda=1)
        
        # Temporarily remove the redraw functionality on the matrix to interact with the final state
        shrinkage_matrix_mobj.clear_updaters() 
        
        # We need to get the entries of the final matrix state
        final_matrix = shrinkage_matrix_mobj.submobjects[0]
        
        # Identify the off-diagonal entries (indices 1 and 2 for a 2x2 matrix, excluding the brackets)
        # Manim's Matrix Mobject returns its inner components as a VGroup
        # For a 2x2, indices are typically: [0]=Bracket, [1]=Entries (VGroup)
        entries = final_matrix.get_entries()
        
        # Highlight the off-diagonal entries (entries[1] and entries[2])
        off_diagonal_rects = VGroup(
            SurroundingRectangle(entries[1], color=YELLOW, buff=0.1),
            SurroundingRectangle(entries[2], color=YELLOW, buff=0.1)
        )
        
        text_explanation = Text(
            "Covariances shrunk to zero ($\lambda=1$)", 
            font_size=30
        ).to_edge(DOWN)

        self.play(
            Create(off_diagonal_rects),
            Write(text_explanation)
        )
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(VGroup(formula, lambda_label, shrinkage_matrix_mobj, 
                           off_diagonal_rects, text_explanation))
        )
        self.wait(1)
