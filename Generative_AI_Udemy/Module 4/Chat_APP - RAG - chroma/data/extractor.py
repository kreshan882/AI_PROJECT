from bs4 import BeautifulSoup
import re

def extract_tirukkural(html_file, output_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Preprocess: Add line breaks after </center> tags to separate them from kural numbers
    html_content = re.sub(r'</center>\s*', '</center>\n<br>', html_content)
    
    # Preprocess: Ensure separators are on their own line
    html_content = re.sub(r'-{3,}', '\n---------\n', html_content)
    
    # Variables to track current title and subtitle
    current_title = ""
    current_subtitle = ""
    
    # Dictionary to store all kurals
    kural_dict = {}
    
    # Split by <br> tags
    lines = re.split(r'<br\s*/?>', html_content, flags=re.IGNORECASE)
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Parse the line
        soup_line = BeautifulSoup(line, 'html.parser')
        line_text = soup_line.get_text().strip()
        
        # Check for sections with red/blue font (titles and subtitles)
        if 'font color="red"' in line or 'font color="blue"' in line:
            # Skip PART I, II, III
            if 'PART I' in line_text or 'PART II' in line_text or 'PART III' in line_text:
                i += 1
                continue
            
            # Extract title (1.1 Title)
            title_match = re.search(r'(\d+\.\d+)\s+([A-Z][^\n\d]+?)(?=\s*\d+\.\d+\.\d+|$)', line_text)
            if title_match:
                current_title = title_match.group(2).strip()
            
            # Extract subtitle (1.1.1 Subtitle or 1.1.2. Subtitle)
            subtitle_match = re.search(r'\d+\.\d+\.\d+\.?\s+(.+?)$', line_text)
            if subtitle_match:
                current_subtitle = subtitle_match.group(1).strip()
            
            i += 1
            continue
        
        # Check for kural number - be very specific
        # Must be ONLY digits with optional period, possibly with whitespace
        kural_match = re.match(r'^\s*(\d+)\.?\s*$', line_text)
        
        if kural_match:
            kural_num = int(kural_match.group(1))
            
            # Must be in valid range
            if 1 <= kural_num <= 1330:
                verse_lines = []
                meaning = ""
                
                # Look ahead to collect verse and meaning
                j = i + 1
                content_lines = 0
                
                while j < len(lines) and content_lines < 30:
                    next_line = lines[j]
                    next_soup = BeautifulSoup(next_line, 'html.parser')
                    next_text = next_soup.get_text().strip()
                    
                    # Skip empty lines
                    if not next_text or len(next_text) < 2:
                        j += 1
                        continue
                    
                    # Skip separator lines
                    if re.match(r'^-+$', next_text):
                        j += 1
                        continue
                    
                    content_lines += 1
                    
                    # Stop if we hit another kural number (after collecting some content)
                    if re.match(r'^\s*(\d+)\.?\s*$', next_text) and content_lines > 2:
                        potential_next = int(re.match(r'^\s*(\d+)\.?\s*$', next_text).group(1))
                        if 1 <= potential_next <= 1330:
                            break
                    
                    # Stop if we hit a new section header (after collecting content)
                    if ('<center>' in next_line or 'font color=' in next_line) and content_lines > 3:
                        break
                    
                    # Check for meaning in <i> or <em> tags
                    italic = next_soup.find(['i', 'em'])
                    if italic and not meaning:
                        meaning = italic.get_text().strip()
                        j += 1
                        # If we have verse and meaning, we're done
                        if len(verse_lines) >= 2:
                            break
                        continue
                    
                    # Collect verse lines (must contain actual words)
                    if re.search(r'[a-zA-Z]{3,}', next_text):
                        # Skip if it's a section number
                        if not re.match(r'^\d+\.\d+', next_text):
                            # Skip if it's in italic (that's the meaning)
                            if not italic:
                                verse_lines.append(next_text)
                    
                    j += 1
                    
                    # Stop after we have complete content
                    if len(verse_lines) >= 2 and meaning:
                        break
                
                # Save the kural if we have content
                if verse_lines or meaning:
                    verse_text = '\n'.join(verse_lines[:2]) if len(verse_lines) >= 2 else '\n'.join(verse_lines)
                    
                    kural_dict[kural_num] = {
                        'title': current_title,
                        'subtitle': current_subtitle,
                        'verse': verse_text,
                        'meaning': meaning
                    }
        
        i += 1
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for kural_num in sorted(kural_dict.keys()):
            kural_data = kural_dict[kural_num]
            f.write(f"Title: {kural_data['title']}\n")
            f.write(f"Sub Title: {kural_data['subtitle']}\n")
            f.write(f"Kural {kural_num}: {kural_data['verse']}\n")
            f.write(f"Meaning: {kural_data['meaning']}\n")
            f.write(f"</kural>\n\n")
    
    print(f"Extracted {len(kural_dict)} kurals to {output_file}")
    
    # Check for missing
    missing = [i for i in range(1, 1331) if i not in kural_dict]
    if missing:
        print(f"\n⚠ Missing {len(missing)} kurals")
        
        # Analyze pattern
        ending_in_1 = [k for k in missing if k % 10 == 1]
        if ending_in_1:
            print(f"Pattern: {len(ending_in_1)} kurals ending in '1' are missing")
        
        if len(missing) <= 50:
            print(f"Missing: {missing}")
        else:
            print(f"First 30 missing: {missing[:30]}")
            print(f"Last 10 missing: {missing[-10:]}")
    else:
        print("\n✓ SUCCESS! All 1330 kurals extracted!")
    
    if kural_dict:
        print(f"Range: {min(kural_dict.keys())} to {max(kural_dict.keys())}")

if __name__ == "__main__":
    input_file = "tirukkuRaL, English translation and commentary by Rev. G.U. Pope, Drew, Lazarus and Ellis.html"
    output_file = "tirukkural_output.txt"
    
    extract_tirukkural(input_file, output_file)