Page {
    title: "Now"
    padding: "8"
    scrollable: "true"
    
    Column {
        padding: "8"
        //Image { src: "happy.png" }

        Spacer {amount: 16}
        Markdown {
            part: "now.md"
        }
        Spacer { weight: 1}
        
        Row {
            Button {label: "< What's Wrong" link: "page:whatswrong" weight: 1}
            Spacer {amount: 8}
            Button {label: "Todo >" link: "page:home" weight: 1}
        }
    }
}