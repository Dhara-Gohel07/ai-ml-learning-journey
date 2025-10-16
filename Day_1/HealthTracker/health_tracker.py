class HealthUser:
    def __init__(self, name, age, gender,weight, height):
        self.name = name
        self.age = age
        self.gender = gender
        self.weight = weight  # in kg
        self.height = height  # in feet

    def greet(self):
        return f"Hello, {self.name}! Welcome to the Health Tracker."
    
    def advice_category(self):
        if self.age<18:
            return "teen"
        elif self.age<65:
            return "adult"
        else:
            return "senior"
class HealthAdvisor(HealthUser):
    def __init__(self,name, age, gender, weight, height,tips_file="health_tips.txt"):
        super().__init__(name, age,gender, weight, height)
        self.tips_file = tips_file
        self.tips = self.load_tips()

    def load_tips(self):
        try :
            with open(self.tips_file, 'r') as file :
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"File {self.tips_file} not found.")
            return []
    
    def get_advice(self):
        category = self.advice_category()
        print(f"Personalized advice for {self.name} ({category}):")
        if category == "teen":
            print("- Focus on sleep blanced diet")
            self.show_tips(3)
        if category == "adult":
            print("- Regular exercise ,stay hydrated,manage stress")
            self.show_tips(5)
        if category == "senior":
            print("- Regular health check-ups and genetal exercise")
            self.show_tips(3)

        self.show_bmi()
        self.calorie_advice()

    def show_tips(self, count):
        import random
        selected_tips = random.sample(self.tips, min(count, len(self.tips)))
        for tip in selected_tips:
            print(f"- {tip}")

    def calculate_bmi(self):
        # assuming height is in feet
        height_in_meters = self.height * 0.3048
        bmi = self.weight / (height_in_meters ** 2)
        return round(bmi, 2), round(self.height, 2)  # returns (bmi, height in feet)

    def show_bmi(self):
        bmi, height_in_feet = self.calculate_bmi()
        print(f"Your BMI is: {bmi}")
        if bmi < 18.5:
            print("You are underweight. Consider a balanced diet to gain weight.")
        elif 18.5 <= bmi < 24.9:
            print("You have a normal weight. Keep up the good work!")
        elif 25 <= bmi < 29.9:
            print("You are overweight. Consider a healthy diet and regular exercise.")
        else:
            print("You are obese. It's advisable to consult a healthcare provider for guidance.")

    def calorie_advice(self):
        if self.age < 18:
            calories = 2200
        elif self.age < 65:
            if self.gender == "male":
                calories = 2500
            else:
                calories = 2000
        else:
            calories = 1800
        print(f"Recommended daily calorie intake: {calories} calories.") 

def main():
    print("== Health Tracker ==")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ").lower()
    weight = float(input("Enter your weight (in kg): "))
    height = float(input("Enter your height (in feet): "))    
    
    advisor = HealthAdvisor(name, age, gender, weight, height) 
    advisor.greet()           
    advisor.get_advice()    
    print("Goodbye!")

if __name__ == "__main__":
    main()