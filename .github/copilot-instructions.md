# Code Quality
All code you write MUST be fully optimized. 'Fully optimized' includes maximizing algorithmic big-O efficiency for memory and runtime, following proper style conventions for the code, language (e.g. maximizing code reuse (DRY)), and no extra code beyond what is absolutely necessary to solve the problem the user provides (i.e. no technical debt).

# Context Management
Avoid making assumptions. If you need additional context to accurately answer the user, ask the user for the missing information. Be specific about which context you need.

# File Organization
Always provide the name of the file in your response so the user knows where the code goes. Use descriptive names that clearly indicate the purpose of the file. Follow consistent naming conventions throughout the project. Use appropriate file extensions. Avoid special characters or spaces in file names - use hyphens or underscores instead. Keep names concise while maintaining clarity.

# Code Modularity
Break code up into modules and components for reuse across the project. Follow these principles:
- Single Responsibility: Each module should have one clear purpose
- Encapsulation: Hide implementation details, expose clean interfaces
- Loose Coupling: Minimize dependencies between modules
- Clear Interfaces: Make APIs easy to understand
- Consistent Naming: Use clear conventions
- Documentation: Thoroughly document purpose and usage
