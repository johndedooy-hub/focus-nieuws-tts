import urllib.request
import xml.etree.ElementTree as ET

# Een stabiele, openbare EDM-podcastbron (Corsten's Countdown / Ferry Corsten of alternatief archief)
RSS_URL = "https://danceonair.com"
OUTPUT_FILE = "edm_releases.m3u"

def fetch_edm_releases():
    try:
        # HTTP-header toevoegen zodat de server ons verzoek niet blokkeert
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        response = urllib.request.urlopen(req)
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
            title_element = item.find('title')
            title = title_element.text if title_element is not None else "Unknown EDM Track"
            
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
