"""
Euler's Derivative Identity Visualization: f(x) = a^x and Its Derivative

This animation demonstrates the unique property of Euler's number e where 
the function f(x) = e^x is equal to its own derivative. The visualization 
shows the transition from a general exponential function a^x (where a ≠ e) 
to the special case when a = e, highlighting how the function and its 
derivative become identical.

Key concepts illustrated:
1. For f(x) = a^x, the derivative is f'(x) = ln(a) * a^x
2. When a = e, ln(e) = 1, so f'(x) = e^x = f(x)
3. The animation shows real-time values and slope comparisons as 'a' approaches e
"""

from manim import *
import numpy as np

class EulerNumber(Scene):
    def construct(self):
        """
        Main animation method that builds the visualization step by step.
        
        The animation consists of:
        1. Setting up titles and coordinate axes
        2. Creating dynamic graphs that update with parameter changes
        3. Displaying real-time calculations and comparisons
        4. Animating the transition from a=2 to a=e
        5. Demonstrating the perfect match between function and derivative at a=e
        """
        
        # ===========================================
        # Step 1: Setup Titles and Coordinate System
        # ===========================================
        
        # Main title explaining the concept
        title = Text("The Magic of Euler's Number: e", font_size=36, color=BLUE)
        title.to_edge(UP, buff=0.3)  # Position at top of screen
        
        # Create coordinate axes for graphing
        axes = Axes(
            x_range=[-3, 3, 1],      # x-axis from -3 to 3 with unit ticks
            y_range=[0, 15, 5],      # y-axis from 0 to 15 with 5-unit ticks
            x_length=9,              # Horizontal size
            y_length=5,              # Vertical size
            axis_config={"include_tip": True, "color": WHITE}
        ).shift(DOWN * 0.5)          # Shift down slightly for better layout
        
        # ===========================================
        # Step 2: Create Value Trackers for Animation
        # ===========================================
        
        # Tracker for the base 'a' of the exponential function
        # Start with a = 2.0 to show the difference before reaching e
        a_tracker = ValueTracker(2.0)
        
        # Tracker for the x-coordinate along the curve
        x_tracker = ValueTracker(0.0)
        
        # ===========================================
        # Step 3: Create Dynamic Graphs
        # ===========================================
        
        # Function graph: f(x) = a^x
        # Uses always_redraw to update automatically when 'a' changes
        graph = always_redraw(lambda: 
            axes.plot(
                lambda x: a_tracker.get_value()**x,  # a^x function
                x_range=[-3, 2.3],                   # Domain to plot
                color=YELLOW,                        # Function color
                stroke_width=5                       # Thicker line for visibility
            )
        )
        
        # Derivative graph: f'(x) = ln(a) * a^x
        # Also updates automatically with 'a'
        deriv_graph = always_redraw(lambda: 
            axes.plot(
                lambda x: np.log(a_tracker.get_value()) * (a_tracker.get_value()**x),
                x_range=[-3, 2.3],                   # Same domain
                color=RED,                           # Derivative color
                stroke_width=3,                      # Slightly thinner
                stroke_opacity=0.7                   # Semi-transparent for overlay
            )
        )

        # ===========================================
        # Step 4: Create Dynamic UI Elements
        # ===========================================
        
        # Helper functions for real-time calculations
        def get_val():
            """Calculate current function value: a^x"""
            return a_tracker.get_value()**x_tracker.get_value()
        
        def get_slope():
            """Calculate current derivative value: ln(a) * a^x"""
            return np.log(a_tracker.get_value()) * (a_tracker.get_value()**x_tracker.get_value())

        # Top Left Box: Real-time numerical values display
        # Shows base, function value, and slope (derivative)
        data_display = always_redraw(lambda:
            VGroup(
                # Base value display
                VGroup(
                    Text("Base a =", font_size=22),
                    DecimalNumber(a_tracker.get_value(), num_decimal_places=3, color=GREEN)
                ).arrange(RIGHT),
                
                # Separator line
                Line(LEFT, RIGHT).scale(1.5).set_stroke(width=1, color=GRAY),
                
                # Function value display
                VGroup(
                    Text("f(x) value =", font_size=20, color=YELLOW),
                    DecimalNumber(get_val(), color=YELLOW)
                ).arrange(RIGHT),
                
                # Derivative/slope display
                VGroup(
                    Text("Slope f'(x) =", font_size=20, color=RED),
                    DecimalNumber(get_slope(), color=RED)
                ).arrange(RIGHT),
            ).arrange(DOWN, aligned_edge=LEFT).to_edge(UL, buff=0.7)  # Position in top-left corner
        )

        # Bottom Right Box: Euler identity status indicator
        # Shows whether we're at the special case (a = e) or not
        identity_label = always_redraw(lambda:
            VGroup(
                # Label text
                Text("Relationship Status:", font_size=18, color=GRAY),
                
                # Status indicator - "IDENTICAL" when a ≈ e, "PROPORTIONAL" otherwise
                Text(
                    "IDENTICAL" if abs(a_tracker.get_value() - np.exp(1)) < 0.01 else "PROPORTIONAL", 
                    font_size=28,
                    color=GREEN if abs(a_tracker.get_value() - np.exp(1)) < 0.01 else WHITE
                )
            ).arrange(DOWN).to_edge(DR, buff=0.7).shift(UP * 0.5)  # Position in bottom-right
        )

        # ===========================================
        # Step 5: Create Visual Elements
        # ===========================================
        
        # Moving dot on the function curve
        dot = always_redraw(lambda: 
            Dot(
                axes.c2p(x_tracker.get_value(), get_val()),  # Position at current (x, f(x))
                color=WHITE
            )
        )
        
        # Tangent line at the current point
        tangent = always_redraw(lambda:
            Line(
                # Start point: slightly left of current x
                start=axes.c2p(x_tracker.get_value() - 0.8, get_val() - get_slope() * 0.8),
                # End point: slightly right of current x
                end=axes.c2p(x_tracker.get_value() + 0.8, get_val() + get_slope() * 0.8),
                color=PINK,      # Distinct color for tangent
                stroke_width=4   # Visible but not overwhelming
            )
        )

        # ===========================================
        # Step 6: Animation Sequence
        # ===========================================
        
        # Add initial static elements
        self.add(title, axes, graph, deriv_graph, data_display, identity_label)
        
        # Add dynamic elements with creation animations
        self.play(Create(dot), Create(tangent))
        self.wait(1)  # Pause to let viewer see initial setup
        
        # --------------------------------------------------
        # Phase 1: Demonstrate the difference when a ≠ e (a = 2)
        # --------------------------------------------------
        
        # Move along the curve to show function and derivative values at different points
        self.play(x_tracker.animate.set_value(1.2), run_time=3)
        self.wait(1)  # Pause to observe values
        
        # --------------------------------------------------
        # Phase 2: Transform base from 2 to e
        # --------------------------------------------------
        
        # Show explanatory text
        e_note = Text("Transforming base to e...", font_size=24, color=ORANGE).to_edge(DOWN)
        self.play(Write(e_note))
        
        # Animate the base changing from 2 to e
        self.play(a_tracker.animate.set_value(np.exp(1)), run_time=5)
        self.wait(1)  # Pause to observe the transformation
        
        # --------------------------------------------------
        # Phase 3: Highlight the Euler identity achievement
        # --------------------------------------------------
        
        # Emphasize the data display showing identical values
        self.play(Indicate(data_display, scale_factor=1.1), FadeOut(e_note))
        
        # Show confirmation text
        proof_text = Text("At a = e : f(x) and f'(x) merge!", font_size=26, color=GREEN).to_edge(DOWN)
        self.play(Write(proof_text))
        
        # --------------------------------------------------
        # Phase 4: Final demonstration of perfect tracking
        # --------------------------------------------------
        
        # Move along the curve to show that function and derivative remain identical
        # First move left
        self.play(x_tracker.animate.set_value(-1.5), run_time=4)
        
        # Then move right
        self.play(x_tracker.animate.set_value(1.5), run_time=4)
        
        # Final pause to let viewer absorb the concept
        self.wait(4)