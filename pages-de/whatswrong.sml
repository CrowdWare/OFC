Page {
    title: "Whats Wrong"
    padding: "8"
    scrollable: "true"
    
    Column {
        padding: "8"

        //Image { src: "magic_book.png" }

        Spacer {amount: 16}
        Markdown {
            part: "whatswrong.md"
        }
        Spacer {amount: 8}
        Row {
            Button {label: "< Gift" link: "page:gift" weight: 1}
            Spacer {amount: 8}
            Button {label: "Now >" link: "page:now" weight: 1}
        }
    }
}