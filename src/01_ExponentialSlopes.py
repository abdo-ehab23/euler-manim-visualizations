"""
Euler Number Visualization: Exponential Functions and Their Slopes

This animation demonstrates the relationship between exponential functions 
(2^x and 3^x) and their derivatives. It visualizes how the slope of these 
functions is proportional to their value, with constants k₁ ≈ 0.693 (ln 2) 
and k₂ ≈ 1.099 (ln 3). The animation shows tangent lines, slope triangles, 
and real-time calculations to illustrate that d/dx(a^x) = k·a^x, where k = ln(a).

The visual explores why there exists a special number 'e' (approximately 2.718) 
where k = 1, meaning the function equals its own derivative.
"""

from manim import *

class ExponentialSlopes(MovingCameraScene):
    # ==============================
    # Helper Functions
    # ==============================
    
    def get_slope_angle(self, fun, x):
        """
        Calculate the angle of the slope (derivative) at a given x-value.
        
        Args:
            fun: The function to evaluate
            x: The x-coordinate where to calculate the slope
        
        Returns:
            angle: The angle in radians of the tangent line at point x
        """
        # Numerical derivative using finite difference approximation
        df = lambda x: (fun(x + 1e-6) - fun(x)) / 1e-6
        slope = df(x)  # Calculate the derivative (slope)
        angle = np.arctan(slope)  # Convert slope to angle
        return angle
    
    def get_tangent_line(self, ax: Axes, fun, x: float, length: float = 40, color=RED) -> Line:
        """
        Create a tangent line to the function at point x.
        
        Args:
            ax: The coordinate axes
            fun: The function to tangent to
            x: The x-coordinate of tangency point
            length: Visual length of the tangent line
            color: Color of the tangent line
        
        Returns:
            line: A Line object representing the tangent
        """
        # Compute line parameters using the slope angle
        half_length = length / 2
        angle = self.get_slope_angle(fun, x)
        
        # Calculate x and y components of the line
        dx = half_length * np.cos(angle)
        dy = half_length * np.sin(angle)
        
        # Calculate start and end points in pixel coordinates
        start = ax.c2p(x - dx, fun(x) - dy)
        end = ax.c2p(x + dx, fun(x) + dy)
        
        # Create and style the line
        line = Line(start, end, color=color)
        line.set_stroke(width=2)
        return line
    
    def get_slope_line1(self, ax: Axes, fun, x):
        """
        Create the vertical dashed line for the slope triangle (rise component).
        This line represents the change in y-value over a unit x-interval.
        
        Args:
            ax: The coordinate axes
            fun: The function
            x: Starting x-coordinate
        
        Returns:
            line: Dashed vertical line for slope visualization
        """
        x_a = x + 1  # Endpoint x-coordinate (one unit to the right)
        y_a = np.tan(self.get_slope_angle(fun, x)) + fun(x)  # Corresponding y-value
        
        # Convert to pixel coordinates
        p1 = ax.c2p(x_a, fun(x))  # Start point (on function)
        p2 = ax.c2p(x_a, y_a)     # End point (on tangent line)
        
        # Create dashed line for visual clarity
        line = DashedLine(p1, p2, stroke_width=2, dash_length=.1, dashed_ratio=.9)
        return line

    def get_slope_line2(self, ax: Axes, fun, x):
        """
        Create the horizontal dashed line for the slope triangle (run component).
        This line represents the unit interval in the x-direction.
        
        Args:
            ax: The coordinate axes
            fun: The function
            x: Starting x-coordinate
        
        Returns:
            line: Dashed horizontal line for slope visualization
        """
        x_a = x + 1  # Endpoint x-coordinate
        
        # Convert to pixel coordinates
        p1 = ax.c2p(x_a, fun(x))  # End point
        p2 = ax.c2p(x, fun(x))    # Start point
        
        # Create dashed line
        line = DashedLine(p2, p1, stroke_width=2, dash_length=.1, dashed_ratio=.9)
        return line
    
    def print_label1(self, ax, line, offset=RIGHT*0.2):
        """
        Create a dynamic label for the vertical slope component (rise).
        The label shows the absolute vertical distance between line endpoints.
        
        Args:
            ax: The coordinate axes
            line: The line to label
            offset: Position offset for the label
        
        Returns:
            label: Always-updating DecimalNumber for the rise value
        """
        return always_redraw(
            lambda: DecimalNumber(
                abs(ax.p2c(line.get_end())[1] - ax.p2c(line.get_start())[1]),
                num_decimal_places=2,
                font_size=24
            ).next_to(line.get_center(), offset)
        )

    def print_label2(self, ax, line, offset=DOWN*0.2):
        """
        Create a dynamic label for the horizontal slope component (run).
        The label shows the absolute horizontal distance between line endpoints.
        
        Args:
            ax: The coordinate axes
            line: The line to label
            offset: Position offset for the label
        
        Returns:
            label: Always-updating DecimalNumber for the run value
        """
        return always_redraw(
            lambda: DecimalNumber(
                abs(ax.p2c(line.get_end())[0] - ax.p2c(line.get_start())[0]),
                num_decimal_places=2,
                font_size=24
            ).next_to(line.get_center(), offset)
        )
    
    # ==============================
    # Main Visualization Function
    # ==============================
    
    def create_function_elements(self, ax, fun, color, moving_dot, 
                                 x_range=(-2.5, 3.5), text_offset=RIGHT*0.3, 
                                 dot_color=ORANGE, base_value=None):
        """
        Create all visualization elements for an exponential function.
        
        This function generates:
        - The function graph
        - Moving tracking dot
        - Axis projection dots
        - Coordinate labels
        - Tangent line
        - Slope triangle lines
        - Slope value labels
        - Function label
        
        Args:
            ax: Coordinate axes
            fun: Exponential function to visualize
            color: Color scheme for this function
            moving_dot: Identifier for the moving dot
            x_range: Domain range for plotting
            text_offset: Position offset for function label
            dot_color: Color of the moving dot
            base_value: Base of the exponential function (2 or 3)
        
        Returns:
            dict: Dictionary containing all visualization elements
        """
        # Create the function graph
        graph = ax.plot(fun, color=color, x_range=x_range)
        
        # Create moving dot that tracks along the curve
        moving_dot_obj = Dot(ax.i2gp(graph.t_min, graph), color=dot_color)
        
        # Create dots that project onto axes
        dot1 = Dot(ax.c2p(ax.x_range[0], 0), radius=.05)  # x-axis projection
        dot2 = Dot(ax.c2p(0, ax.y_range[0]), radius=.05)  # y-axis projection
        
        # Updaters to keep projection dots aligned with moving dot
        dot1.add_updater(lambda m: m.move_to(ax.c2p(
            ax.p2c(moving_dot_obj.get_center())[0], 0)))
        dot2.add_updater(lambda m: m.move_to(ax.c2p(
            0, ax.p2c(moving_dot_obj.get_center())[1])))
        
        # Dynamic labels for x and y coordinates
        x_label = always_redraw(lambda: DecimalNumber(
            ax.p2c(dot1.get_center())[0],
            num_decimal_places=2,
            font_size=18
        ).next_to(dot1, DOWN))
        
        y_label = always_redraw(lambda: DecimalNumber(
            ax.p2c(dot2.get_center())[1],
            num_decimal_places=2,
            font_size=18
        ).next_to(dot2, LEFT))
        
        # Dynamic tangent line that updates with moving dot
        tangent = always_redraw(lambda: self.get_tangent_line(
            ax, fun, x=ax.p2c(moving_dot_obj.get_center())[0]))
        
        # Dynamic slope triangle components
        slope_line1 = always_redraw(lambda: self.get_slope_line1(
            ax, fun, x=ax.p2c(moving_dot_obj.get_center())[0]))
        
        slope_line2 = always_redraw(lambda: self.get_slope_line2(
            ax, fun, x=ax.p2c(moving_dot_obj.get_center())[0]))
        
        # Labels for slope components
        label1 = self.print_label1(ax, slope_line1)  # Rise label
        label2 = self.print_label2(ax, slope_line2)  # Run label
        
        # Function label (2^x or 3^x)
        if base_value:
            fun_text = MathTex(fr"{base_value}^{{x}}", font_size=28, color=color)
        elif fun(1) == 2:  # Identify 2^x function
            fun_text = MathTex(r"2^x", font_size=28, color=color)
        else:  # Identify 3^x function
            fun_text = MathTex(r"3^x", font_size=28, color=color)
        fun_text.next_to(graph.point_from_proportion(0.7), text_offset)
        
        # Return all elements as a structured dictionary
        return {
            'graph': graph,
            'moving_dot': moving_dot_obj,
            'dots': [dot1, dot2],
            'labels': [x_label, y_label],
            'tangent': tangent,
            'slope_lines': [slope_line1, slope_line2],
            'slope_labels': [label1, label2],
            'fun_text': fun_text,
            'all_elements': VGroup(moving_dot_obj, dot1, dot2, x_label, y_label, 
                                   tangent, slope_line1, slope_line2, label1, label2)
        }
    
    # ==============================
    # Main Animation Sequence
    # ==============================
    
    def construct(self):
        """
        Main animation construction method.
        
        This method orchestrates the entire visualization:
        1. Shows 2^x function with slope analysis (k₁ = ln 2 ≈ 0.693)
        2. Shows 3^x function with slope analysis (k₂ = ln 3 ≈ 1.099)
        3. Compares both to illustrate the search for base e where k = 1
        """
        
        # ===========================================
        # Step 1: Setup and First Function (2^x)
        # ===========================================
        
        # Create coordinate axes
        ax = Axes(x_range=[-10, 10], y_range=[-10, 20])
        
        # Create visualization elements for 2^x
        fun1 = lambda x: np.power(2, x)
        elements1 = self.create_function_elements(
            ax, fun1, BLUE, "moving_dot1", 
            x_range=[-2.5, 3.5], text_offset=RIGHT*0.3,
            base_value=2  # Explicit base value for labeling
        )
        
        # Create visualization elements for 3^x (hidden initially)
        fun2 = lambda x: np.power(3, x)
        elements2 = self.create_function_elements(
            ax, fun2, GREEN, "moving_dot2", 
            x_range=[-2.5, 2.7], text_offset=RIGHT*0.5,
            base_value=3  # Explicit base value for labeling
        )
        
        # Animate the creation of axes and 2^x graph
        self.play(
            LaggedStart(
                Create(ax),
                Create(elements1['graph']),
                lag_ratio=0.7
            ),
            run_time=2
        )
        
        # Show the function label 2^x
        self.play(Write(elements1['fun_text']))
        
        # Add moving dot and axis projection dots
        self.play(
            LaggedStart(
                FadeIn(elements1['moving_dot'], scale=0.5),
                FadeIn(elements1['dots'][0], scale=0.5),
                FadeIn(elements1['dots'][1], scale=0.5),
                lag_ratio=0.4
            ),
            run_time=1
        )
        
        # Add coordinate labels
        self.add(*elements1['labels'])
        
        # Create tangent line and slope triangle
        self.play(
            LaggedStart(
                Create(elements1['tangent']),
                Create(elements1['slope_lines'][0]),
                Create(elements1['slope_lines'][1]),
                lag_ratio=0.2,
            ),
            run_time=2
        )
        
        # Add slope value labels
        self.add(*elements1['slope_labels'])
        
        # Force initial update of slope labels
        elements1['slope_labels'][0].update()
        elements1['slope_labels'][1].update()
        
        # ===========================================
        # Step 2: Mathematical Analysis for 2^x
        # ===========================================
        
        # Create text annotations in top-left corner for 2^x analysis
        # Line 1: General slope equation
        txt1_line1 = MathTex(r"\text{slope} = k_1 \cdot 2^x", font_size=24, color=RED)
        txt1_line1.move_to(ax.c2p(-7, 11))  # Position in top-left
        
        # Line 2: Real-time numerical values
        values_text1 = always_redraw(
            lambda: MathTex(
                rf"{np.log(2)*np.power(2,ax.p2c(elements1['moving_dot'].get_center())[0]):.2f} = "
                rf"k_1 \cdot 2^{{{ax.p2c(elements1['moving_dot'].get_center())[0]:.2f}}}",
                font_size=24,
                color=RED
            ).next_to(txt1_line1, DOWN, buff=0.2).align_to(txt1_line1, LEFT)
        )
        
        # Line 3: Constant value k₁ = ln 2
        k1_text = MathTex("k_1=0.693", font_size=24, color=RED)
        k1_text.next_to(values_text1, DOWN, buff=0.2).align_to(txt1_line1, LEFT)
        
        # Animate the mathematical text
        self.play(
            LaggedStart(
                Write(txt1_line1),
                Write(values_text1),
                Write(k1_text),
                lag_ratio=0.4
            ),
            run_time=1
        )
        
        # Add a background grid for better spatial reference
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1.2,
                "stroke_opacity": 0.4
            },
            axis_config={"stroke_opacity": 0}
        )
        
        self.play(LaggedStart(Create(grid), lag_ratio=0.2), run_time=.5)
        
        # ===========================================
        # Step 3: Animate Movement Along 2^x Curve
        # ===========================================
        
        # Move the dot along the 2^x curve to demonstrate changing slope
        self.play(self.camera.frame.animate.scale(1))
        self.play(
            MoveAlongPath(elements1['moving_dot'], elements1['graph'], rate_func=smooth),
            run_time=7
        )
        self.wait(1)  # Pause for observation
        
        # ===========================================
        # Step 4: Transition to Second Function (3^x)
        # ===========================================
        
        # Fade out dynamic elements of 2^x (keep curve and text)
        elements_to_fade = VGroup(
            elements1['moving_dot'],
            elements1['dots'][0],
            elements1['dots'][1],
            elements1['labels'][0],
            elements1['labels'][1],
            elements1['tangent'],
            elements1['slope_lines'][0],
            elements1['slope_lines'][1],
            elements1['slope_labels'][0],
            elements1['slope_labels'][1]
        )
        
        self.play(FadeOut(elements_to_fade))
        self.wait(1)
        
        # Zoom out to accommodate both functions
        self.play(self.camera.frame.animate.scale(1.8))
        
        # Fade in 3^x curve
        self.play(FadeIn(elements2['graph']))
        
        # Position and show 3^x label behind the curve
        elements2['fun_text'].set_z_index(-1)
        self.play(Write(elements2['fun_text']))
        
        # Add all 3^x visualization elements at once
        self.add(elements2['moving_dot'])
        self.add(*elements2['dots'])
        self.add(*elements2['labels'])
        self.add(elements2['tangent'])
        self.add(*elements2['slope_lines'])
        self.add(*elements2['slope_labels'])
        
        # Update slope labels to show correct initial values
        elements2['slope_labels'][0].update()
        elements2['slope_labels'][1].update()
        
        # ===========================================
        # Step 5: Mathematical Analysis for 3^x
        # ===========================================
        
        # Create text annotations for 3^x ABOVE the 2^x text
        # Line 1: General slope equation for 3^x
        txt2_line1 = MathTex(r"\text{slope} = k_2 \cdot 3^x", font_size=24, color=PURPLE)
        txt2_line1.move_to(ax.c2p(-7, 13))  # Above 2^x text
        
        # Line 2: Real-time numerical values for 3^x
        values_text2 = always_redraw(
            lambda: MathTex(
                rf"{np.log(3)*np.power(3,ax.p2c(elements2['moving_dot'].get_center())[0]):.2f} = "
                rf"k_2 \cdot 3^{{{ax.p2c(elements2['moving_dot'].get_center())[0]:.2f}}}",
                font_size=24,
                color=PURPLE
            ).next_to(txt2_line1, DOWN, buff=0.2).align_to(txt2_line1, LEFT)
        )
        
        # Line 3: Constant value k₂ = ln 3
        k2_text = MathTex("k_2=1.099", font_size=24, color=PURPLE)
        k2_text.next_to(values_text2, DOWN, buff=0.2).align_to(txt2_line1, LEFT)
        
        # Move 2^x text down to make room
        self.play(
            txt1_line1.animate.shift(DOWN * 1),
            values_text1.animate.shift(DOWN * 1),
            k1_text.animate.shift(DOWN * 1)
        )
        
        # Show 3^x mathematical text
        self.play(
            LaggedStart(
                Write(txt2_line1),
                Write(values_text2),
                Write(k2_text),
                lag_ratio=0.4
            ),
            run_time=1
        )
        
        # ===========================================
        # Step 6: Animate Movement Along 3^x Curve
        # ===========================================
        
        # Move the dot along the 3^x curve
        self.play(
            MoveAlongPath(elements2['moving_dot'], elements2['graph'], rate_func=smooth),
            run_time=7
        )
        self.wait(1)
        
        # Zoom in for final comparison
        self.play(self.camera.frame.animate.scale(1))
        
        # ===========================================
        # Step 7: Clean Up and Final Comparison
        # ===========================================
        
        # Fade out dynamic elements of 3^x
        elements_to_fade_2 = VGroup(
            elements2['moving_dot'],
            elements2['dots'][0],
            elements2['dots'][1],
            elements2['labels'][0],
            elements2['labels'][1],
            elements2['tangent'],
            elements2['slope_lines'][0],
            elements2['slope_lines'][1],
            elements2['slope_labels'][0],
            elements2['slope_labels'][1]
        )
        
        self.play(FadeOut(elements_to_fade_2))
        self.wait(1)
        
        # Final zoom for emphasis
        self.play(self.camera.frame.animate.scale(.5))
        self.wait(1)
        
        # ===========================================
        # Step 8: Side-by-Side Comparison
        # ===========================================
        
        # Group texts for final arrangement
        final_texts = VGroup(
            VGroup(txt2_line1, values_text2, k2_text),  # 3^x group
            VGroup(txt1_line1, values_text1, k1_text)   # 2^x group
        )
        
        # Arrange texts side by side for comparison
        self.play(
            final_texts[0].animate.shift(LEFT * 1),   # Move 3^x left
            final_texts[1].animate.shift(RIGHT * 1),  # Move 2^x right
            run_time=1
        )
        
        # Adjust vertical positioning for better visibility
        self.play(
            final_texts[0].animate.shift(DOWN * .4),  # Lower 3^x slightly
            final_texts[1].animate.shift(UP * 1),     # Raise 2^x
            run_time=1
        )
        
        # Final pause to observe the comparison
        self.wait(4)