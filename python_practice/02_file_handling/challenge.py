# ==============================================================================
# challenge.py - Server Access Log Analyzer
# ==============================================================================
# CHALLENGE: Read the server log file, count log levels (INFO, WARNING, ERROR),
# and export all warnings and errors into a clean file called `error_report.txt`.

import os

# Helper function to generate mock server log files for testing
def create_mock_logs(filename):
    logs = [
        "2026-06-20 12:00:01 [INFO] User login successful for admin",
        "2026-06-20 12:01:15 [INFO] GET /api/v1/posts request received",
        "2026-06-20 12:02:40 [WARNING] Database connection latency detected (1.5s)",
        "2026-06-20 12:03:10 [INFO] GET /api/v1/posts returned status 200",
        "2026-06-20 12:05:00 [ERROR] Connection refused to MySQL Database at localhost:3306",
        "2026-06-20 12:05:30 [INFO] Re-attempting database connection (Attempt 1)",
        "2026-06-20 12:06:12 [ERROR] Failed to fetch user profile: Key ID invalid",
        "2026-06-20 12:08:45 [WARNING] Memory usage exceeded 85% limit on host server",
        "2026-06-20 12:10:00 [INFO] Scheduled database backups completed successfully"
    ]
    with open(filename, "w") as file:
        for entry in logs:
            file.write(entry + "\n")
    print(f"Generated sample server log file: {filename}")


# Main log parser function to implement
def analyze_logs(log_filename, report_filename):
    """
    Reads the file log_filename line-by-line, counts the frequency of log levels 
    (INFO, WARNING, ERROR), and writes all [WARNING] and [ERROR] lines to report_filename.
    
    Prints a summary table showing log counts.
    """
    # Create the sample log file if it does not exist
    if not os.path.exists(log_filename):
        create_mock_logs(log_filename)
        
    # Counters for different levels
    info_count = 0
    warning_count = 0
    error_count = 0
    
    # Store critical messages for writing
    critical_messages = []
    
    # Read the log file line by line
    with open(log_filename, "r") as file:
        for line in file:
            # Check for severity levels in the log line
            if "[INFO]" in line:
                info_count += 1
            elif "[WARNING]" in line:
                warning_count += 1
                critical_messages.append(line)
            elif "[ERROR]" in line:
                error_count += 1
                critical_messages.append(line)

    # Write warnings and errors to the error report file
    with open(report_filename, "w") as report_file:
        report_file.write("=== LOG ERROR & WARNING REPORT ===\n")
        report_file.write(f"Total Warnings: {warning_count}\n")
        report_file.write(f"Total Errors: {error_count}\n")
        report_file.write("==================================\n\n")
        for message in critical_messages:
            report_file.write(message)
            
    # Print the analysis summary to the console
    print("\n==================================")
    print("        LOG ANALYSIS SUMMARY      ")
    print("==================================")
    print(f" INFO logs:     {info_count}")
    print(f" WARNING logs:  {warning_count}")
    print(f" ERROR logs:    {error_count}")
    print("==================================")
    print(f"Report generated: '{report_filename}'")
    print("==================================")


if __name__ == "__main__":
    log_file = "server_logs.txt"
    report_file = "error_report.txt"
    analyze_logs(log_file, report_file)

# ------------------------------------------------------------------------------
# 🏆 Extension Challenges for You:
# 1. Modify the script to count how many logs happened at each hour (e.g. 12:00, 12:01, etc.).
# 2. Add dynamic terminal arguments (using standard python module `sys`) so you can type:
#    `python challenge.py custom_logs.txt report.txt` to parse custom files.
# ------------------------------------------------------------------------------
