const studyTopics = {

    OS: [
        "Process Scheduling",
        "Threads",
        "Paging",
        "Memory Management",
        "Disk Scheduling"
    ],

    DBMS: [
        "SQL",
        "ER Diagram",
        "Normalization",
        "Transactions",
        "Indexing"
    ],

    DAA: [
        "Sorting",
        "Greedy Algorithms",
        "Dynamic Programming",
        "Backtracking",
        "Graph Algorithms"
    ],

    CN: [
        "OSI Model",
        "TCP/IP",
        "Routing",
        "Transport Layer",
        "Network Security"
    ]
};


function createPlan() {

    let subject = document.getElementById("subject").value.toUpperCase();

    let days = Number(document.getElementById("days").value);

    let hours = Number(document.getElementById("hours").value);

    let plan = document.getElementById("plan");


    if (subject === "" || days === 0 || hours === 0) {

        plan.innerHTML = "<p>Please enter all details.</p>";

        return;
    }


    let topics = studyTopics[subject];


    if (!topics) {

        plan.innerHTML = `
            <h2>Study Plan</h2>
            <p>Subject not found.</p>
            <p>Please try OS, DBMS, DAA or CN.</p>
        `;

        return;
    }


    let result = "<h2>📅 Your Study Plan</h2>";


    let planDays = Math.min(days, 5);


    for (let day = 1; day <= planDays; day++) {

        result += `<h3>Day ${day}</h3>`;

        result += `<p>Study Time: ${hours} hours</p>`;


        let start = (day - 1) * 2;

        let selectedTopics = topics.slice(start, start + 2);


        if (selectedTopics.length === 0) {

            result += "<p>📖 Revision</p>";
            result += "<p>📝 Mock Test</p>";

        } else {

            selectedTopics.forEach(function(topic) {

                result += `<p>☐ ${topic}</p>`;

            });


            if (day === planDays) {

                result += "<p>📝 Revision + Mock Test</p>";

            } else {

                result += "<p>📖 Learn + Practice</p>";

            }
        }
    }


    plan.innerHTML = result;
}
