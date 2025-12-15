from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random

# Set window size
Window.size = (450, 700)

class RockPaperScissorsGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Set background color
        with self.canvas.before:
            Color(0.2, 0.25, 0.3, 1)  # Dark blue-gray background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Game state variables
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds_played = 0
        
        # Title
        self.title = Label(
            text='🎮 Rock Paper Scissors',
            font_size='32sp',
            size_hint=(1, 0.12),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.add_widget(self.title)
        
        # Score display
        self.score_label = Label(
            text=self.get_score_text(),
            font_size='20sp',
            size_hint=(1, 0.1),
            color=(0.3, 0.8, 1, 1)
        )
        self.add_widget(self.score_label)
        
        # Instructions
        self.instruction_label = Label(
            text='Choose your move:',
            font_size='22sp',
            size_hint=(1, 0.08),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.instruction_label)
        
        # Choice buttons (Rock, Paper, Scissors)
        button_layout = GridLayout(
            cols=3,
            spacing=10,
            size_hint=(1, 0.15)
        )
        
        # Rock button
        self.rock_btn = Button(
            text='🪨\nRock',
            font_size='18sp',
            background_color=(0.7, 0.3, 0.3, 1),
            background_normal=''
        )
        self.rock_btn.bind(on_press=lambda x: self.play_game('Rock'))
        button_layout.add_widget(self.rock_btn)
        
        # Paper button
        self.paper_btn = Button(
            text='📄\nPaper',
            font_size='18sp',
            background_color=(0.3, 0.7, 0.3, 1),
            background_normal=''
        )
        self.paper_btn.bind(on_press=lambda x: self.play_game('Paper'))
        button_layout.add_widget(self.paper_btn)
        
        # Scissors button
        self.scissors_btn = Button(
            text='✂️\nScissors',
            font_size='18sp',
            background_color=(0.3, 0.3, 0.7, 1),
            background_normal=''
        )
        self.scissors_btn.bind(on_press=lambda x: self.play_game('Scissors'))
        button_layout.add_widget(self.scissors_btn)
        
        self.add_widget(button_layout)
        
        # Result display area
        result_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.35),
            spacing=10
        )
        
        # Player choice display
        self.player_choice_label = Label(
            text='Your choice: -',
            font_size='20sp',
            size_hint=(1, 0.3),
            color=(1, 0.9, 0.4, 1)
        )
        result_container.add_widget(self.player_choice_label)
        
        # Computer choice display
        self.computer_choice_label = Label(
            text='Computer choice: -',
            font_size='20sp',
            size_hint=(1, 0.3),
            color=(1, 0.9, 0.4, 1)
        )
        result_container.add_widget(self.computer_choice_label)
        
        # Result message
        self.result_label = Label(
            text='Make your choice!',
            font_size='28sp',
            size_hint=(1, 0.4),
            color=(1, 1, 1, 1),
            bold=True
        )
        result_container.add_widget(self.result_label)
        
        self.add_widget(result_container)
        
        # Action buttons
        action_layout = GridLayout(
            cols=2,
            spacing=10,
            size_hint=(1, 0.12)
        )
        
        # Reset scores button
        self.reset_btn = Button(
            text='🔄 Reset Scores',
            font_size='18sp',
            background_color=(0.8, 0.5, 0.2, 1),
            background_normal=''
        )
        self.reset_btn.bind(on_press=self.reset_game)
        action_layout.add_widget(self.reset_btn)
        
        # Play again button
        self.play_again_btn = Button(
            text='▶️ Play Again',
            font_size='18sp',
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        self.play_again_btn.bind(on_press=self.clear_for_new_round)
        action_layout.add_widget(self.play_again_btn)
        
        self.add_widget(action_layout)
        
        # Stats display
        self.stats_label = Label(
            text='Start playing to see stats!',
            font_size='16sp',
            size_hint=(1, 0.08),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.add_widget(self.stats_label)
    
    def _update_rect(self, instance, value):
        """Update background rectangle when window size changes"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def get_score_text(self):
        """Format the score display"""
        return f'You: {self.user_score}  |  Computer: {self.computer_score}  |  Ties: {self.ties}'
    
    def get_choice_emoji(self, choice):
        """Return emoji for each choice"""
        emojis = {
            'Rock': '🪨',
            'Paper': '📄',
            'Scissors': '✂️'
        }
        return emojis.get(choice, '')
    
    def play_game(self, user_choice):
        """Main game logic - this is where the magic happens!"""
        # Computer makes a random choice
        choices = ['Rock', 'Paper', 'Scissors']
        computer_choice = random.choice(choices)
        
        # Update the display
        self.player_choice_label.text = f'Your choice: {self.get_choice_emoji(user_choice)} {user_choice}'
        self.computer_choice_label.text = f'Computer choice: {self.get_choice_emoji(computer_choice)} {computer_choice}'
        
        # Determine the winner
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update scores
        if result == 'win':
            self.user_score += 1
            self.result_label.text = '🎉 You Win!'
            self.result_label.color = (0.2, 1, 0.2, 1)  # Green
        elif result == 'lose':
            self.computer_score += 1
            self.result_label.text = '😢 You Lose!'
            self.result_label.color = (1, 0.2, 0.2, 1)  # Red
        else:
            self.ties += 1
            self.result_label.text = '🤝 It\'s a Tie!'
            self.result_label.color = (1, 1, 0.2, 1)  # Yellow
        
        # Update rounds played
        self.rounds_played += 1
        
        # Update displays
        self.score_label.text = self.get_score_text()
        self.update_stats()
    
    def determine_winner(self, user, computer):
        """
        Game logic: Rock beats Scissors, Scissors beats Paper, Paper beats Rock
        Returns: 'win', 'lose', or 'tie'
        """
        if user == computer:
            return 'tie'
        
        # All winning combinations for the user
        winning_combos = {
            'Rock': 'Scissors',      # Rock beats Scissors
            'Paper': 'Rock',         # Paper beats Rock
            'Scissors': 'Paper'      # Scissors beats Paper
        }
        
        if winning_combos[user] == computer:
            return 'win'
        else:
            return 'lose'
    
    def update_stats(self):
        """Update the statistics display"""
        if self.rounds_played > 0:
            win_rate = (self.user_score / self.rounds_played) * 100
            self.stats_label.text = f'Rounds: {self.rounds_played} | Win Rate: {win_rate:.1f}%'
    
    def reset_game(self, instance):
        """Reset all scores and start fresh"""
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds_played = 0
        
        self.score_label.text = self.get_score_text()
        self.stats_label.text = 'Start playing to see stats!'
        self.player_choice_label.text = 'Your choice: -'
        self.computer_choice_label.text = 'Computer choice: -'
        self.result_label.text = 'Make your choice!'
        self.result_label.color = (1, 1, 1, 1)
    
    def clear_for_new_round(self, instance):
        """Clear the display for a new round without resetting scores"""
        self.player_choice_label.text = 'Your choice: -'
        self.computer_choice_label.text = 'Computer choice: -'
        self.result_label.text = 'Make your choice!'
        self.result_label.color = (1, 1, 1, 1)


class RockPaperScissorsApp(App):
    def build(self):
        self.title = 'Rock Paper Scissors Game'
        return RockPaperScissorsGame()


# Run the app
if __name__ == '__main__':
    RockPaperScissorsApp().run()