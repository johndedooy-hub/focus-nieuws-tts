import urllib.request
import xml.etree.ElementTree as ET

# Een publieke EDM podcast feed die directe MP3-links bevat
RSS_URL = "https://podspace.space"
OUTPUT_FILE = "edm_releases.m3u"

def fetch_edm_releases():
    try:
        # Haal de RSS feed op
        response = urllib.request.urlopen(RSS_URL)
        data = response.read()
        
        # Parse de XML data
        root = ET.fromstring(data)
        
        # Zoek alle 'item' elementen (de tracks/episodes)
        items = root.findall('.//item')
        
        # Pak de laatste 10 releases
        latest_items = items[:10]
        
        # Bouw de M3U structuur
        m3u_content = "#EXTM3U\n"
        
        for item in latest_items:
            title = item.find('title').text
            
            # Zoek naar de audio link (enclosure tag)
            enclosure = item.find('enclosure')
            if enclosure is not None and 'url' in enclosure.attrib:
                audio_url = enclosure.attrib['url']
                
                # Voeg toe aan M3U formaat
                m3u_content += f"#EXTINF:-1,{title}\n"
                m3u_content += f"{audio_url}\n"
        
        # Sla het bestand op
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"Succes! {OUTPUT_FILE} is aangemaakt met de laatste 10 releases.")
        
    except Exception as e:
        print(f"Er ging iets mis: {e}")

if __name__ == "__main__":
    fetch_edm_releases()
  
