from waveshare_epd import epd2in13_V3
import time
from PIL import Image, ImageDraw, ImageFont
import os

class DisplayManager:
    def __init__(self):
        self.epd = epd2in13_V3.EPD()
        self.width = 250
        self.height = 122
        self.font_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        
    def init_display(self):
        self.epd.init()
        self.epd.Clear(0xFF)
        
    def get_fonts(self):
        try:
            # Utiliser une police par défaut si la police personnalisée n'est pas disponible
            default_font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
            custom_font = os.path.join(self.font_dir, 'Font.ttc')
            
            font_path = custom_font if os.path.exists(custom_font) else default_font
            
            if not os.path.exists(font_path):
                raise FileNotFoundError(f"Aucune police trouvée: ni personnalisée ni par défaut")
                
            title_font = ImageFont.truetype(font_path, 16)
            normal_font = ImageFont.truetype(font_path, 12)
            return title_font, normal_font
            
        except Exception as e:
            print(f"Erreur de chargement des polices: {str(e)}")
            # Utiliser une police par défaut intégrée à PIL comme solution de repli
            return ImageFont.load_default(), ImageFont.load_default()
        
    def create_display_image(self, stats_data):
        image = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(image)
        title_font, normal_font = self.get_fonts()
        
        # Draw title with timestamp
        draw.text((5, 5), f"NiceHash Stats", font=title_font, fill=0)
        draw.text((5, 25), stats_data['timestamp'], font=normal_font, fill=0)
        
        # Draw mining stats
        draw.text((5, 45), f"Active Rigs: {stats_data['active_rigs']}", font=normal_font, fill=0)
        draw.text((5, 60), f"Total Hashrate: {stats_data['total_hashrate']}", font=normal_font, fill=0)
        
        # Draw wallet balances
        y_pos = 80
        for currency, balance in stats_data['balances'].items():
            draw.text((5, y_pos), f"{currency}: {balance}", font=normal_font, fill=0)
            y_pos += 15
        
        # Draw EUR balance
        if 'balance_eur' in stats_data:
            draw.text((5, y_pos), f"EUR: {stats_data['balance_eur']}", font=normal_font, fill=0)
            
        return image
        
    def update_display(self, stats_data):
        try:
            self.init_display()
            image = self.create_display_image(stats_data)
            self.epd.display(self.epd.getbuffer(image))
        except Exception as e:
            print(f"Display Error: {str(e)}")
        finally:
            self.epd.sleep()