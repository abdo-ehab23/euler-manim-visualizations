"""
Euler's Formula Visualization: 3D Propagation of e^(iθ)

This animation provides a geometric visualization of Euler's formula:
    e^(iθ) = cos(θ) + i·sin(θ)

The visualization shows:
1. The complex exponential as a point moving around a unit circle
2. How this circular motion propagates along the θ-axis to create helices
3. The projection of this motion onto real (cosine) and imaginary (sine) components
4. The relationship between circular motion in the complex plane and sinusoidal waves

The animation transitions between different perspectives to reveal how
trigonometric functions emerge from the complex exponential function.
"""

from manim import *

class EulerPropagation(ThreeDScene):
    def construct(self):
        """
        Main animation sequence for visualizing Euler's formula.
        
        The animation unfolds in several phases:
        1. Introduction of Euler's formula
        2. Circular motion in the complex plane
        3. Propagation along θ-axis forming a helix
        4. Isolation of sine and cosine components
        5. Final synthesis of the relationship
        """
        
        # ===========================================
        # Phase 1: Title and Formula Introduction
        # ===========================================
        
        # Create title and Euler's formula
        title = Text("Euler's Formula", font_size=36)
        formula = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=42)
        
        # Group and position title elements in top-left corner
        full_title = VGroup(title, formula).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        full_title.to_corner(UL).shift(RIGHT*0.5 + DOWN*0.3)  # Fine-tuned to avoid overlap
        
        # Add title to fixed frame (won't move with 3D camera)
        self.add_fixed_in_frame_mobjects(full_title)
        self.play(Write(full_title), run_time=2)
        self.wait(1)  # Pause for viewer to read
        
        # ===========================================
        # Phase 2: Setup 3D Coordinate System
        # ===========================================
        
        # Create 3D coordinate axes
        axes = ThreeDAxes(
            x_range=[-2, 10, 1],   # θ-axis range (horizontal propagation)
            y_range=[-3, 3, 1],    # Imaginary axis (vertical)
            z_range=[-3, 3, 1],    # Real axis (depth)
            x_length=10,
            y_length=6,
            z_length=6,
        )
        
        # Label axes: θ (angle), Im (imaginary), Re (real)
        axes_labels = axes.get_axis_labels(x_label="\\theta", y_label="Im", z_label="Re")
        
        # ===========================================
        # Phase 3: Initial Circle (Complex Plane)
        # ===========================================
        
        # Unit circle representing e^(iθ) in the complex plane
        circle = Circle(radius=1, color=BLUE_E).move_to(axes.c2p(0, 0, 0))
        circle_label = MathTex(r"e^{i\theta}", color=BLUE_E, font_size=48).next_to(circle, UP)
        
        # Moving point on the circle (complex exponential)
        dot = Dot3D(color=YELLOW, radius=0.1).move_to(axes.c2p(0, 1, 0))
        
        # Traced paths for cosine (real) and sine (imaginary) components
        cos_trace = TracedPath(dot.get_center, stroke_width=8, stroke_color=RED)
        sin_trace = TracedPath(dot.get_center, stroke_width=8, stroke_color=GREEN)
        
        # ===========================================
        # Phase 4: Helix for Propagation Along θ
        # ===========================================
        
        # Parametric helix showing propagation along θ-axis
        # As θ increases, the circular motion propagates forward
        helix = ParametricFunction(
            lambda t: axes.c2p(t/(2*PI)*3, np.sin(t), np.cos(t)),  # Parametric: (θ, sinθ, cosθ)
            t_range=[0, 4*PI],      # Two full rotations
            color=BLUE_E
        )
        
        # ===========================================
        # Phase 5: Initial Setup Animation
        # ===========================================
        
        # Set initial camera angle (top-down view of complex plane)
        self.set_camera_orientation(phi=75*DEGREES, theta=-90*DEGREES)
        
        # Animate creation of axes and circle
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(circle), Write(circle_label))
        
        # Add traces and dot (start recording the path)
        self.add(cos_trace, sin_trace, dot)
        self.wait(1)  # Brief pause
        
        # ===========================================
        # Phase 6: Circular Motion in Complex Plane
        # ===========================================
        
        # Rotate dot around circle (two full rotations)
        # This shows e^(iθ) tracing the unit circle
        self.play(
            Rotate(dot, angle=4*PI, about_point=ORIGIN, axis=RIGHT),
            run_time=8,
            rate_func=linear  # Constant speed
        )
        self.wait(1)  # Pause to observe circular trace
        
        # ===========================================
        # Phase 7: Horizontal Propagation (Helix Formation)
        # ===========================================
        
        # Transform circle into helix and move dot along it
        # This shows how circular motion propagates along θ-axis
        self.play(
            Transform(circle, helix),   # Circle morphs into helix
            MoveAlongPath(dot, helix),  # Dot follows helix path
            run_time=12,
            rate_func=linear
        )
        self.play(FadeOut(circle_label))  # Remove old label
        
        # ===========================================
        # Phase 8: 3D Overview of the Helix
        # ===========================================
        
        # Change camera angle to show 3D perspective of helix
        self.move_camera(phi=70*DEGREES, theta=30*DEGREES, run_time=4)
        self.wait(1)  # Pause for 3D observation
        
        # ===========================================
        # Phase 9: Cosine (Real Component) Reveal
        # ===========================================
        
        # Reset camera to side view (focus on real/imaginary plane)
        self.move_camera(phi=0*DEGREES, theta=0*DEGREES, run_time=5)
        
        # Change colors to red theme to highlight cosine component
        self.play(
            cos_trace.animate.set_color(RED).set_stroke(width=12),  # Emphasize cosine trace
            sin_trace.animate.set_color(RED_D),                     # Dim sine trace
            helix.animate.set_color(RED_C),                         # Color helix red
            dot.animate.set_color(RED),                             # Red dot
            axes.animate.set_color(RED_E),                          # Red axes
            run_time=2
        )
        
        # Display "sin θ" label (though we're highlighting cosine - showing contrast)
        sin_big = Text("sin θ", color=GREEN, font_size=80).to_edge(DOWN).shift(RIGHT*3)
        self.add_fixed_in_frame_mobjects(sin_big)
        self.play(Write(sin_big), run_time=2)
        self.wait(4)  # Pause with label
        self.play(FadeOut(sin_big))  # Remove label
        
        # ===========================================
        # Phase 10: Reset Colors for Next Phase
        # ===========================================
        
        # Restore original colors
        self.play(
            cos_trace.animate.set_color(RED).set_stroke(width=8),  # Normal width
            sin_trace.animate.set_color(GREEN),                    # Restore green
            helix.animate.set_color(BLUE_E),                       # Restore blue
            dot.animate.set_color(YELLOW),                         # Restore yellow
            axes.animate.set_color(WHITE),                         # White axes
            run_time=1.5
        )
        
        # ===========================================
        # Phase 11: Sine (Imaginary Component) Reveal
        # ===========================================
        
        # Change camera to top view (focus on imaginary plane)
        self.move_camera(phi=90*DEGREES, theta=-90*DEGREES, run_time=5)
        
        # Change colors to green theme to highlight sine component
        self.play(
            sin_trace.animate.set_color(GREEN).set_stroke(width=12),  # Emphasize sine trace
            cos_trace.animate.set_color(GREEN_D),                     # Dim cosine trace
            helix.animate.set_color(GREEN_C),                         # Color helix green
            dot.animate.set_color(GREEN),                             # Green dot
            axes.animate.set_color(GREEN_E),                          # Green axes
            run_time=2
        )
        
        # Display "cos θ" label (showing contrast with sine)
        cos_big = Text("cos θ", color=RED, font_size=80).to_edge(DOWN).shift(RIGHT*3)
        self.add_fixed_in_frame_mobjects(cos_big)
        self.play(Write(cos_big), run_time=2)
        self.wait(3)  # Pause with label
        self.play(FadeOut(cos_big))  # Remove label
        
        # ===========================================
        # Phase 12: Final Conclusion
        # ===========================================
        
        # Display concluding message
        conclusion = Text("One complex circle →\ncos θ and sin θ waves", 
                         font_size=44, line_spacing=1.2)
        conclusion.to_corner(DL)  # Bottom-left corner
        
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        
        # Final pause to let viewer absorb the complete relationship
        self.wait(5)