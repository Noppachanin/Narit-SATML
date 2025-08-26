import numpy as np
# from datetime import datetime,timedelta
import pandas as pd
from io import StringIO  # Import StringIO
import time
import matplotlib.pyplot as plt
import spacetrack.operators as op
from spacetrack import SpaceTrackClient
from datetime import datetime,timedelta



def tle_epoch_to_datetime(epoch: str) -> datetime:
    """
    Converts a TLE epoch string (YYDDD.fractionalday) to a datetime object.

    Args:
        epoch (str): The TLE epoch string in the format YYDDD.fractionalday.

    Returns:
        datetime: The corresponding datetime object.

    Raises:
        ValueError: If the epoch string is invalid or the year is invalid.
    """
    if not isinstance(epoch, str) or len(epoch) < 5:
        raise ValueError("Invalid TLE epoch format. Must be YYDDD.fractionalday.")

    year_str = epoch[:2]
    day_str = epoch[2:]

    try:
        year = int(year_str)
        day_of_year = float(day_str)
    except ValueError:
        raise ValueError("Invalid TLE epoch format.  Must be YYDDD.fractionalday.")

    if year < 0 or year > 99:
        raise ValueError("Invalid TLE year.  Must be 0-99.")

    # Determine the century
    century = 2000 if year < 57 else 1900  # Year 57 is the cutoff

    # Calculate the full year.
    full_year = century + year

    # Create a datetime object for the beginning of the year
    start_of_year = datetime(full_year, 1, 1)

    # Calculate the timedelta for the day of year (including fractional part)
    day_delta = timedelta(days=day_of_year - 1)  # Subtract 1 as the year starts on day 1

    # Add the timedelta to the start of the year
    # (year, month, day, hour=0, minute=0, second=0)
    return start_of_year + day_delta


def tle_to_dataframe(tle_data_string):
    """
    Parses a string containing TLE data into a Pandas DataFrame.

    Args:
        tle_data_string (str): A string containing TLE data in the standard two-line format.

    Returns:
        pandas.DataFrame: A DataFrame containing the parsed TLE data.  Returns an empty
                        DataFrame if the input string is empty or only contains headers.
    """
    # Ensure the input is a string
    if not isinstance(tle_data_string, str):
        raise TypeError("Input must be a string.")

    # Use StringIO to treat the string as a file
    tle_file = StringIO(tle_data_string)

    # Read the lines from the string
    lines = tle_file.readlines()

    if not lines:
        return pd.DataFrame()  # Return an empty DataFrame for empty input

    # Initialize lists to store the data
    data = []
    header_names = [
        "Satellite Name", "Epoch", 
        "First Derivative Mean Motion", "Second Derivative Mean Motion",
        "BSTAR Drag Term", "Element Set Number", "Inclination (degrees)",
        "Right Ascension of the Ascending Node (degrees)", "Eccentricity",
        "Argument of Perigee (degrees)", "Mean Anomaly (degrees)",
        "Mean Motion (revolutions per day)", "Revolution Number at Epoch"
    ]

    # Process TLE lines in pairs
    for i in range(0, len(lines) - 1, 2):
        try:
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip()

            # Extract data from line 1
            satellite_name = line1[2:18].strip()
            epoch = line1[18:32].strip()
            first_derivative_mean_motion = float(line1[33:43].strip())

            # Handle potential errors in these fields
            second_derivative_mean_motion_str = line1[44:52].replace('-', '-0').strip()
            if second_derivative_mean_motion_str:
                try:
                    second_derivative_mean_motion = float(second_derivative_mean_motion_str)
                except ValueError:
                    second_derivative_mean_motion = 0.0
            else:
                second_derivative_mean_motion = 0.0

            bstar_drag_term_str = line1[53:61].replace('-', '-0').strip()
            if bstar_drag_term_str:
                try:
                    bstar_drag_term = float(bstar_drag_term_str)
                except ValueError:
                    bstar_drag_term = 0.0
            else:
                bstar_drag_term = 0.0
            element_set_number = int(line1[64:68].strip())

            # Extract data from line 2
            inclination = float(line2[8:16].strip())
            raan = float(line2[17:25].strip())
            eccentricity = float("0." + line2[26:33].strip())  # Add leading zero
            arg_of_perigee = float(line2[34:42].strip())
            mean_anomaly = float(line2[43:51].strip())
            mean_motion = float(line2[52:63].strip())
            revolution_number = int(line2[63:68].strip())

            # Append the data as a list
            data.append([
                satellite_name,  epoch,
                first_derivative_mean_motion, second_derivative_mean_motion,
                bstar_drag_term, element_set_number, inclination, raan, eccentricity,
                arg_of_perigee, mean_anomaly, mean_motion, revolution_number
            ])
        except (ValueError, IndexError) as e:
            print(f"Error parsing TLE lines {i+1}-{i+2}: {e}. Skipping these lines.")
            # Handle errors in parsing (e.g., malformed TLE data)
            continue

    # Create the Pandas DataFrame
    df = pd.DataFrame(data, columns=header_names)
    return df


def spactrack_retrieval_to_df(sat_dict, start_date, end_date, email='noppachanin.phys@gmail.com', passwrd='MySpaceTrack1999'):
    
    st = SpaceTrackClient(email, passwrd)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    drange = op.inclusive_range(start_date_str, end_date_str)
    
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            tle_data = st.gp_history(
                norad_cat_id=str(sat_dict['norad_id']),
                creation_date=drange,
                orderby="CREATION_DATE asc", 
                format='tle'
            )
            #     print(len(tle_data))

            out_df = tle_to_dataframe(tle_data)
            break

        except Exception as e:
            retries += 1
            print(f"Retry {retries}, An error occurred: {e}")

        time.sleep(2)
    
    if retries < max_retries:     
        return out_df
    else:
        return None

def spactrack_retrieval(sat_dict, start_date, end_date, email='noppachanin.phys@gmail.com', passwrd='MySpaceTrack1999'):
    
    st = SpaceTrackClient(email, passwrd)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    drange = op.inclusive_range(start_date_str, end_date_str)
    
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            tle_data = st.gp_history(
                norad_cat_id=str(sat_dict['norad_id']),
                creation_date=drange,
                orderby="CREATION_DATE asc", 
                format='tle'
            )
            #     print(len(tle_data))

            break

        except Exception as e:
            retries += 1
            print(f"Retry {retries}, An error occurred: {e}")

        time.sleep(2)
    
    if retries < max_retries:     
        return tle_data
    else:
        return None
    
    
    
def _calculate_checksum(line):
    """
    Calculates the TLE checksum for a single line.
    
    The checksum is the sum of all digits, with a count of 1 for each negative sign.
    """
    checksum = 0
    for char in line:
        if char.isdigit():
            checksum += int(char)
        elif char == '-':
            checksum += 1
    return checksum % 10

def _format_scientific_notation(value):
    """
    Formats a floating-point number into the TLE-specific scientific notation (e.g., 1.2345-5).
    """
    if value == 0:
        return ' 00000-0'
    
    # Get the sign
    sign = '-' if value < 0 else ' '
    
    # Convert to standard scientific notation
    exponent = math.floor(math.log10(abs(value)))
    mantissa = abs(value) / (10**exponent)
    
    # TLE format requires the mantissa to be between 0.1 and 1.
    if mantissa >= 1.0:
        mantissa /= 10
        exponent += 1
    
    mantissa_str = f"{mantissa:.5f}".replace('.', '')
    
    # TLE format has a single-digit exponent
    exponent_sign = '-' if exponent < 0 else '+'
    exponent_val = abs(exponent)
    
    return f"{sign}{mantissa_str}{exponent_sign}{exponent_val}"

def _format_eccentricity(eccentricity):
    """
    Formats eccentricity by dropping the leading '0.' and padding with a space.
    """
    ecc_str = f"{eccentricity:.7f}"[2:] # Remove '0.'
    return f" {ecc_str}"

def dataframe_to_tle(df):
    """
    Reconstructs TLE data from a Pandas DataFrame into the original string format.

    Args:
        df (pandas.DataFrame): A DataFrame containing TLE data. The column names
                               must match those generated by tle_to_dataframe.

    Returns:
        str: A string containing the TLE data in the standard two-line format.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas.DataFrame.")
    
    if df.empty:
        return ""

    tle_lines = []

    for _, row in df.iterrows():
        # --- Format Line 1 ---
        # The line number is always 1, and the satellite catalog number is not available
        # from the DataFrame, so we'll use a placeholder ' '
        line1_template = f"1 {row['Satellite Name']:<16s}{row['Epoch']:<14s}{row['First Derivative Mean Motion']:<10.8f} {_format_scientific_notation(row['Second Derivative Mean Motion'])} {_format_scientific_notation(row['BSTAR Drag Term'])} {row['Element Set Number']:4d} {0:1d}"
        
        # Add the final checksum
        line1_base = line1_template[:68]
        line1_checksum = _calculate_checksum(line1_base)
        line1 = f"{line1_base}{line1_checksum}"
        
        # --- Format Line 2 ---
        # The line number is always 2
        line2_template = f"2 {row['Satellite Name']:<5s}{row['Inclination (degrees)']:>8.4f}{row['Right Ascension of the Ascending Node (degrees)']:>8.4f}{_format_eccentricity(row['Eccentricity']):<8s}{row['Argument of Perigee (degrees)']:>8.4f}{row['Mean Anomaly (degrees)']:>8.4f}{row['Mean Motion (revolutions per day)']:>11.8f}{row['Revolution Number at Epoch']:5d}"
        
        # Add the final checksum
        line2_base = line2_template[:68]
        line2_checksum = _calculate_checksum(line2_base)
        line2 = f"{line2_base}{line2_checksum}"
        
        tle_lines.extend([line1, line2])
        
    return "\n".join(tle_lines)


def epoch_to_datatime(df, sort_by_ep=True):
    df['Epoch Date'] = df['Epoch'].apply(lambda x : tle_epoch_to_datetime(x).date())
    df['Epoch Time'] = df['Epoch'].apply(lambda x : tle_epoch_to_datetime(x).time())
    df['Epoch'] = df['Epoch'].apply(lambda x : tle_epoch_to_datetime(x))
    df.sort_values(by='Epoch', ascending=True, inplace=sort_by_ep)
    
    return df

def resampling_tle_df(df):
    
    df.set_index('Epoch', inplace=True)
    
    if isinstance(df.index, pd.DatetimeIndex):
        resample_tle_df = df.select_dtypes(include='number').resample('D').mean().copy()
        resample_tle_df.dropna(inplace=True)
        return resample_tle_df
        
    
    else:
        print(f' Return None')
        return None
    