console.log("==== Task 1 ====");
function findAndPrint(messages) {
  for (const [person, message] of Object.entries(messages)) {
    if (
      ["18", "legal", "college", "vote"].some((keyword) =>
        message.includes(keyword)
      )
    ) {
      console.log(person);
    }
  }
}

findAndPrint({
  Bob: "My name is Bob. I'm 18 years old.",
  Mary: "Hello, glad to meet you.",
  Copper: "I'm a college student. Nice to meet you.",
  Leslie: "I am of legal age in Taiwan.",
  Vivian: "I will vote for Donald Trump next week",
  Jenny: "Good morning.",
});

// ==== Task 2 ====
console.log("==== Task 2 ====");
function calculateSumOfBonus(data) {
  // Write down your bonus rules in comments
  // Rule 1: based on the position
  // - For Engineers, the bonus is 10% of their salary.
  // - For CEOs with average performance, the bonus is 2% of their salary.
  // - For Sales employees with below-average performance, the bonus is 10% of their salary.
  // - For other roles, the bonus is 5% of their salary.

  // Rule 2: based on the performance
  // - For above average, the bonus + 50%.
  // - For average, no extra bonus.
  // - For below average, the bonus -20%.

  // My code here, based on your own rules
  var sumOfBonus = 0;
  var exchangeRate = 30;

  // Loop through each employee
  data.employees.forEach(function (employee) {
    var salary = String(employee.salary);
    var performance = employee.performance;
    var role = employee.role;

    // Convert salary to TWD if it's in USD
    if (salary.includes("USD")) {
      salary = parseInt(salary.replace(/[^0-9]/g, "")) * exchangeRate;
    } else {
      salary = parseInt(salary.replace(/[^0-9]/g, ""));
    }

    // Calculate bonus based on the rules
    var bonus;
    if (role === "Engineer") {
      bonus = 0.1 * salary;
    } else if (role === "CEO") {
      bonus = 0.02 * salary;
    } else if (role === "Sales") {
      bonus = 0.1 * salary;
    } else {
      bonus = 0.05 * salary;
    }

    if (performance === "above average") {
      bonus *= 1.5;
    } else if (performance === "average") {
      bonus *= 1;
    } else if (performance === "below average") {
      bonus *= 0.8;
    }
    // Add the bonus to the total sum
    sumOfBonus += bonus;
  });
  // Print the sum of bonuses
  console.log(sumOfBonus);
}

// call calculateSumOfBonus function
calculateSumOfBonus({
  employees: [
    {
      name: "John",
      salary: "1000USD",
      performance: "above average",
      role: "Engineer",
    },
    {
      name: "Bob",
      salary: 60000,
      performance: "average",
      role: "CEO",
    },
    {
      name: "Jenny",
      salary: "50,000",
      performance: "below average",
      role: "Sales",
    },
  ],
});

// ==== Task 3 ====
console.log("==== Task 3 ====");

function func(...data) {
  // Initialize an object to store the count and the name
  var middleNames = {};
  var nameRecord = {};

  // Loop through each name
  data.forEach((name) => {
    // Check if the name has a middle name
    if (name.length >= 2) {
      // Get the middle name (second word)
      var middleName = name[1];
      // count the middle name
      middleNames[middleName] = (middleNames[middleName] ?? 0) + 1;
      nameRecord[middleName] = name;
    }
  });

  // Find the middle name with a count = 1
  var uniqueMiddleName = null;
  for (var n in middleNames) {
    if (middleNames.hasOwnProperty(n) && middleNames[n] === 1) {
      uniqueMiddleName = nameRecord[n];
    }
  }

  // Print the unique middle name if found, or "沒有" (null) otherwise
  console.log(uniqueMiddleName || "沒有");
}

func("彭⼤牆", "王明雅", "吳明"); // print 彭⼤牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有

// ==== Task 4 ====
console.log("==== Task 4 ====");

function getNumber(index) {
  // Calculate the nth term based on the pattern
  let nthTerm;
  if (index % 2 === 0) {
    nthTerm = (index / 2) * 3;
  } else {
    nthTerm = Math.floor(index / 2) * 3 + 4;
  }

  // Print the nth term
  console.log(Math.floor(nthTerm));
}

getNumber(1); // print 4
getNumber(5); // print 10
getNumber(10); // print 15

// ==== Task 5 ====
console.log("==== Task 5 ====");
function findIndexOfCar(seats, status, number) {
  let car_index = -1;

  for (let i = 0; i < seats.length; i++) {
    if (status[i] === 1 && number <= seats[i]) {
      if (car_index === -1 || seats[i] < seats[car_index]) {
        car_index = i;
      }
    }
  }
  console.log(car_index);
}

findIndexOfCar([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2); // print 4
findIndexOfCar([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1
findIndexOfCar([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
