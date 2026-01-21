def format_time_duration(duration: int, start_with: int = 0, use_abbreviation: bool = False, delimiter: str = ", ") -> str:
    """
    Format time duration in nanoseconds to a human-readable string.

    Args:
        duration (int): Time duration in nanoseconds.
        start_with (int, optional): The minimum level required for the selection when you want to format, 
                                  the range is [0,9). Defaults to 0.
        use_abbreviation (bool, optional): Whether to use abbreviations for time units. Defaults to False.

    Returns:
        str: Formatted time duration string.
    """
    if start_with not in range(0, 10):
        raise ValueError("start_with must be in range [0, 9)")
    
    # Handle zero duration
    if duration == 0:
        return "0 ns" if use_abbreviation else "0 nanoseconds"
    
    # Handle negative duration
    is_negative = duration < 0
    duration = abs(duration)
    
    levels: list[tuple[str, str, int]] = [
        ("nanosecond", "ns", 1000),
        ("microsecond", "μs", 1000),
        ("millisecond", "ms", 1000),
        ("second", "s", 60),
        ("minute", "min", 60),
        ("hour", "h", 24),
        ("day", "day", 30),
        ("month", "mon", 12),
        ("year", "y", 100),
    ]
    end_level: str = "century"
    end_level_abbreviation: str = "cent"
    
    data_level_stack: list[str] = []
    remaining_part: int = duration
    
    # Process each level starting from the specified level
    for name, abbreviation, divisor in levels[start_with:]:
        if remaining_part == 0:
            break
            
        current_value = remaining_part % divisor
        remaining_part //= divisor
        
        if current_value > 0:
            unit = abbreviation if use_abbreviation else name
            # Handle pluralization
            if current_value != 1 and not use_abbreviation:
                unit += "s"
            data_level_stack.append(f"{current_value} {unit}")
        
        if remaining_part == 0:
            break
    
    # Handle the final level (century)
    if remaining_part > 0:
        unit = end_level_abbreviation if use_abbreviation else end_level
        if remaining_part != 1 and not use_abbreviation:
            unit += "s"
        data_level_stack.append(f"{remaining_part} {unit}")
    
    # Reverse the stack to get the correct order (largest to smallest)
    text = delimiter.join(data_level_stack[::-1])
    
    if is_negative:
        text = f"(Negative) {text}"
    
    return text