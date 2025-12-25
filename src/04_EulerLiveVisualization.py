"""
Euler's Formula Live Visualization: Real-time Complex Plane and Wave Analysis

This animation provides a comprehensive real-time visualization of Euler's formula:
    e^(jθ) = cos(θ) + j·sin(θ)

The screen is divided into two main sections:
1. LEFT SIDE: Complex plane showing:
   - Unit circle representing all points with |z| = 1
   - Rotating vector e^(jθ) in yellow
   - Real projection (cosine component) in red
   - Imaginary projection (sine component) in blue

2. RIGHT SIDE: Time-domain waveforms showing:
   - Cosine wave (real part) evolving as θ increases
   - Sine wave (imaginary part) evolving as θ increases

The animation pauses at key angles (90°, 180°, 270°, 360°) to highlight
important values: 1 → j → -1 → -j → 1, and concludes with Euler's famous
identity: e^(jπ) + 1 = 0.
"""

from manim import *
import numpy as np

class EulerLiveVisualization(Scene):
    def construct(self):
        """
        Main animation method for real-time Euler's formula visualization.
        
        The animation shows:
        1. Complex plane with rotating vector and projections
        2. Real-time plotting of cosine and sine waves
        3. Pauses at special angles to highlight important complex values
        4. Culmination with Euler's identity e^(jπ) + 1 = 0
        """
        
        # ===========================================
        # Phase 1: Color Scheme and Styling
        # ===========================================
        
        # Define color scheme for different components
        color_cos = RED      # Cosine/Real part (horizontal projection)
        color_sin = BLUE     # Sine/Imaginary part (vertical projection)
        color_vec = YELLOW   # Complex exponential vector e^(jθ)

        # ===========================================
        # Phase 2: Title Setup
        # ===========================================
        
        # Display Euler's formula as title at top of screen
        title = MathTex("e^{j\\theta} = \\cos(\\theta) + j\\sin(\\theta)", 
                       font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # ===========================================
        # Phase 3: Layout Setup - Two Main Areas
        # ===========================================
        
        # --------------------------------------------------
        # LEFT SIDE: Complex Plane with Unit Circle
        # --------------------------------------------------
        
        # Position for left-side complex plane
        left_origin = LEFT * 3.5 + DOWN * 0.5
        
        # Create complex plane (grid for visualization)
        plane = ComplexPlane(
            x_range=[-2, 2, 1],  # Real axis range
            y_range=[-2, 2, 1],  # Imaginary axis range
            x_length=3.5,        # Horizontal size
            y_length=3.5,        # Vertical size
            axis_config={"stroke_opacity": 0.5}  # Semi-transparent axes
        ).move_to(left_origin)
        
        # Unit circle (all complex numbers with magnitude 1)
        circle = Circle(
            radius=plane.x_axis.get_unit_size(),  # Radius = 1 in plane units
            color=WHITE, 
            stroke_opacity=0.3  # Faint circle for reference
        ).move_to(left_origin)

        # --------------------------------------------------
        # RIGHT SIDE: Time-domain Wave Plots
        # --------------------------------------------------
        
        # Position for right-side waveform plots
        graph_origin = RIGHT * 2 + DOWN * 0.5
        
        # Axes for cosine (real part) waveform
        cos_axes = Axes(
            x_range=[0, TAU, PI/2],     # θ from 0 to 2π with π/2 ticks
            y_range=[-1.2, 1.2],        # Cosine values from -1.2 to 1.2
            x_length=5, y_length=2,     # Size of axes
            axis_config={"include_tip": False}  # No arrow tips
        ).shift(UP * 1.5 + RIGHT * 1.5)  # Position in top-right quadrant
        
        # Axes for sine (imaginary part) waveform
        sin_axes = Axes(
            x_range=[0, TAU, PI/2],     # Same θ range as cosine
            y_range=[-1.2, 1.2],        # Sine values from -1.2 to 1.2
            x_length=5, y_length=2,     # Same size as cosine axes
            axis_config={"include_tip": False}
        ).shift(DOWN * 1.5 + RIGHT * 1.5)  # Position in bottom-right quadrant

        # Labels for the waveform plots
        labels = VGroup(
            MathTex("\\text{Real Part (Cos)}", color=color_cos).scale(0.6).next_to(cos_axes, UP, buff=0.1),
            MathTex("\\text{Imaginary Part (Sin)}", color=color_sin).scale(0.6).next_to(sin_axes, UP, buff=0.1)
        )

        # ===========================================
        # Phase 4: Dynamic Elements Controlled by Time
        # ===========================================
        
        # Time/angle tracker (θ value that increases over time)
        t = ValueTracker(0)

        # --------------------------------------------------
        # LEFT SIDE: Complex Plane Elements
        # --------------------------------------------------
        
        # Main vector: e^(jθ) rotating around unit circle
        vector = always_redraw(lambda: Line(
            left_origin,  # Start at origin
            plane.n2p(np.exp(1j * t.get_value())),  # End at e^(jθ)
            color=color_vec, 
            stroke_width=5
        ).add_tip(tip_length=0.2))  # Add arrow tip

        # Real projection: Horizontal component (cosine)
        real_line = always_redraw(lambda: Line(
            left_origin,  # Start at origin
            plane.n2p(np.cos(t.get_value())),  # End at (cosθ, 0)
            color=color_cos, 
            stroke_width=6
        ))

        # Imaginary projection: Vertical component (sine)
        imag_line = always_redraw(lambda: Line(
            plane.n2p(np.cos(t.get_value())),  # Start at end of real projection
            plane.n2p(np.exp(1j * t.get_value())),  # End at e^(jθ)
            color=color_sin, 
            stroke_width=6
        ))

        # --------------------------------------------------
        # RIGHT SIDE: Waveform Plots
        # --------------------------------------------------
        
        # Cosine wave plotting in real-time as θ increases
        cos_curve = always_redraw(lambda: cos_axes.plot(
            lambda x: np.cos(x),           # Cosine function
            x_range=[0, t.get_value()],    # Plot from 0 to current θ
            color=color_cos
        ))

        # Sine wave plotting in real-time as θ increases
        sin_curve = always_redraw(lambda: sin_axes.plot(
            lambda x: np.sin(x),           # Sine function
            x_range=[0, t.get_value()],    # Plot from 0 to current θ
            color=color_sin
        ))

        # ===========================================
        # Phase 5: Initial Display of All Elements
        # ===========================================
        
        # Create static elements (planes, axes, circle, labels)
        self.play(
            Create(plane), 
            Create(circle), 
            Create(cos_axes), 
            Create(sin_axes), 
            Write(labels)
        )
        
        # Add dynamic elements (they will update automatically)
        self.add(vector, real_line, imag_line, cos_curve, sin_curve)

        # ===========================================
        # Phase 6: Animation with Stops at Key Angles
        # ===========================================
        
        # Key angles and their complex values for demonstration
        stops = [
            (PI/2, "90° = j"),     # θ = π/2: e^(jπ/2) = j
            (PI, "180° = -1"),     # θ = π: e^(jπ) = -1
            (3*PI/2, "270° = -j"), # θ = 3π/2: e^(j3π/2) = -j
            (TAU, "360° = 1")      # θ = 2π: e^(j2π) = 1 (back to start)
        ]

        # Animate through each key angle
        for angle, txt in stops:
            # Create explanatory note for current angle
            note = Text(txt, font_size=24, color=YELLOW).to_corner(DL, buff=1)
            
            # Animate θ increasing to target angle
            self.play(
                t.animate.set_value(angle),  # Update angle tracker
                run_time=2.5,                # Duration for this segment
                rate_func=linear             # Constant angular speed
            )
            
            # Highlight current position and show explanation
            self.play(
                Write(note),                  # Show angle description
                Flash(vector, color=YELLOW)   # Flash the vector for emphasis
            )
            self.wait(1)                      # Pause at this angle
            
            # Remove note before moving to next angle
            self.play(FadeOut(note))

        # ===========================================
        # Phase 7: Final Euler's Identity Display
        # ===========================================
        
        # Display Euler's famous identity: e^(jπ) + 1 = 0
        identity = MathTex("e^{j\\pi} + 1 = 0", color=GOLD).scale(1.5).to_corner(UL).shift(RIGHT * 0.5 + DOWN * 0.5)

        # Create a background rectangle for better visibility
        background_rect = SurroundingRectangle(
            identity, 
            color=BLACK, 
            fill_color=BLACK, 
            fill_opacity=0.7, 
            buff=0.3
        )
        
        # Animate identity appearing with decorative rectangle
        self.play(
            FadeIn(background_rect),          # Black background for contrast
            FadeIn(SurroundingRectangle(identity, color=GOLD)),  # Gold box
            Write(identity)                                       # Identity text
        )
        
        # Final pause to admire the result
        self.wait(4)