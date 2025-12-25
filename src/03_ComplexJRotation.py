"""
Complex Number Rotation: Multiplying by j (Imaginary Unit)

This visualization demonstrates how multiplying by the imaginary unit j
rotates a complex number by 90 degrees in the complex plane. The animation
shows the cyclic pattern of powers of j:
    1 → j → -1 → -j → 1

The animation includes:
1. A complex plane with coordinate system
2. A phasor (arrow) representing a complex number
3. Step-by-step multiplication by j showing 90° rotations
4. Color transitions indicating phase changes
5. Continuous rotation showing the circular trajectory

This demonstrates the fundamental property: j² = -1, and j⁴ = 1.
"""

from manim import *
import numpy as np

class ComplexJRotation(Scene):
    def construct(self):
        """
        Main animation sequence for visualizing complex number rotation by j.
        
        The animation shows:
        1. Setup of complex plane and introductory text
        2. Initial phasor at angle 0 (representing 1)
        3. Four discrete 90° rotations showing the cycle 1→j→-1→-j→1
        4. Continuous rotation showing the circular path
        5. Mathematical equations for each multiplication step
        """
        
        # ===========================================
        # Phase 1: Setup Complex Plane
        # ===========================================
        
        # Create complex plane with coordinate grid
        plane = ComplexPlane(
            x_range=[-2, 2, 1],        # Real axis from -2 to 2
            y_range=[-2, 2, 1],        # Imaginary axis from -2 to 2
            axis_config={"color": WHITE},
            background_line_style={"stroke_opacity": 0.2}  # Faint grid lines
        ).add_coordinates()  # Add coordinate numbers to axes
        
        # Create axis labels with smaller font to avoid overlap
        axes_labels = plane.get_axis_labels(
            x_label=Text("Real", font_size=18).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1),
            y_label=Text("Img", font_size=18).next_to(plane.y_axis.get_top(), UP, buff=0.1)
        )

        # ===========================================
        # Phase 2: Introductory Text
        # ===========================================
        
        # Main explanatory text at top of screen
        intro_text = Text(
            "Multiplying by j rotates the phasor by +90°.",
            font_size=28
        ).to_edge(UP, buff=0.5)  # Position at top with padding

        # ===========================================
        # Phase 3: Angle Tracker for Animation Control
        # ===========================================
        
        # ValueTracker controls the angle of rotation
        # Starts at 0 radians (pointing to 1 on real axis)
        angle_tracker = ValueTracker(0)

        # ===========================================
        # Phase 4: Phasor (Arrow) Representation
        # ===========================================
        
        # Dynamic phasor (arrow) that updates with angle_tracker
        # Represents the complex number e^(jθ)
        phasor = always_redraw(
            lambda: Arrow(
                start=plane.n2p(0),  # Start at origin (0+0j)
                end=plane.n2p(np.exp(1j * angle_tracker.get_value())),  # End at e^(jθ)
                buff=0,              # No buffer at start point
                stroke_width=5,      # Thick line for visibility
                color=self.get_current_color(angle_tracker.get_value())  # Phase-dependent color
            )
        )
        
        # Dot at the tip of the phasor
        dot = always_redraw(lambda: Dot(
            phasor.get_end(), 
            color=phasor.get_color(), 
            radius=0.05
        ))
        
        # Label showing the current complex value (1, j, -1, -j)
        tip_label = MathTex("1", font_size=24).add_updater(
            lambda m: m.next_to(dot, UR, buff=0.05)  # Update position to follow dot
        )

        # ===========================================
        # Phase 5: Initial Display of Elements
        # ===========================================
        
        # Add static elements (plane and labels)
        self.add(plane, axes_labels)
        
        # Animate introductory text
        self.play(Write(intro_text))
        
        # Animate creation of phasor and associated elements
        self.play(GrowArrow(phasor), FadeIn(dot), Write(tip_label))

        # ===========================================
        # Phase 6: Discrete Multiplication Steps (90° Rotations)
        # ===========================================
        
        # Four discrete steps showing the cycle: 1 → j → -1 → -j → 1
        steps = [
            {"angle": PI/2,   "label": "j",  "color": GREEN,  "desc": "1 \\times j = j"},
            {"angle": PI,     "label": "-1", "color": RED,    "desc": "j \\times j = -1"},
            {"angle": 3*PI/2, "label": "-j", "color": PURPLE, "desc": "-1 \\times j = -j"},
            {"angle": 2*PI,   "label": "1",  "color": BLUE,   "desc": "-j \\times j = 1"}
        ]

        # Position for mathematical equations (left side of screen)
        alignment_point = [-1.5, 1, 0]
        
        # Create initial empty math equation at fixed position
        step_math = MathTex("", font_size=28).move_to(alignment_point)
        self.add(step_math)

        # ===========================================
        # Phase 7: Animate Each Step of the Cycle
        # ===========================================
        
        for step in steps:
            # Create new equation for this step
            new_math = MathTex(step["desc"], color=step["color"], font_size=28).move_to(alignment_point)
            
            # Animate rotation and equation update
            self.play(
                angle_tracker.animate.set_value(step["angle"]),  # Rotate phasor
                Transform(step_math, new_math),                   # Update equation
                run_time=1.2
            )
            
            # Update the tip label to show current complex value
            new_label = MathTex(step["label"], color=step["color"], font_size=24).next_to(dot, UR, buff=0.05)
            self.play(Transform(tip_label, new_label), run_time=0.2)
            
            # Pause briefly at each position
            self.wait(0.5)

        # ===========================================
        # Phase 8: Continuous Rotation and Circular Path
        # ===========================================
        
        # Create traced path showing the circular trajectory
        circle_path = TracedPath(
            dot.get_center, 
            stroke_color=WHITE, 
            stroke_width=2, 
            stroke_opacity=0.3  # Semi-transparent
        )
        self.add(circle_path)
        
        # Add explanatory text at bottom
        continuous_info = Text(
            "Circular trajectory in the complex plane", 
            font_size=20, 
            color=YELLOW
        ).to_edge(DOWN, buff=1.0)

        # Animate three full rotations (6π radians)
        self.play(
            angle_tracker.animate.set_value(6 * PI),  # Rotate 3 full circles
            Write(continuous_info),                   # Show explanatory text
            run_time=5,
            rate_func=linear  # Constant angular velocity
        )
        
        # Final pause to observe the complete circular path
        self.wait(2)

    # ===========================================
    # Helper Function: Color Interpolation
    # ===========================================
    
    def get_current_color(self, angle):
        """
        Determine color based on phase angle.
        
        Colors smoothly transition through the rainbow as angle increases:
        0 to π/2:    Blue → Green
        π/2 to π:    Green → Red
        π to 3π/2:   Red → Purple
        3π/2 to 2π:  Purple → Blue
        
        Args:
            angle: Current angle in radians
        
        Returns:
            color: Interpolated color based on phase
        """
        normalized_angle = angle % (2 * PI)  # Wrap to [0, 2π)
        
        # First quadrant: Blue to Green
        if normalized_angle <= PI/2:
            return interpolate_color(BLUE, GREEN, normalized_angle / (PI/2))
        
        # Second quadrant: Green to Red
        elif normalized_angle <= PI:
            return interpolate_color(GREEN, RED, (normalized_angle - PI/2) / (PI/2))
        
        # Third quadrant: Red to Purple
        elif normalized_angle <= 3*PI/2:
            return interpolate_color(RED, PURPLE, (normalized_angle - PI) / (PI/2))
        
        # Fourth quadrant: Purple to Blue (completing the cycle)
        else:
            return interpolate_color(PURPLE, BLUE, (normalized_angle - 3*PI/2) / (PI/2))