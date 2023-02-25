# Terminal Markup
A markup language to build terminal interfaces, built on top of curses.

> ⚠️ This project is purely an experiment and is still under development

## TODO
- [x] debug mode
- [ ] unit/feature testing by dumping curses stdout
- [ ] scrolling
  - [ ] case: parent static max height is 50, child static uses more than 50 lines
- [ ] layout/styles
  - [x] nesting `Statics`
  - [x] auto calculating position and height
  - [ ] flex box
  - [ ] max height
  - [ ] max width
  - [x] min width
  - [x] min height
  - [x] display: inline-block
  - [ ] units (%, cell, line)
  - [ ] CSS parser
- [ ] components
  - [ ] options
  - [ ] text input
  - [ ] button
- [ ] detect mouse input
  - [ ] detect which component was clicked based on cords (focus)

## Known Issues
- The auto calculated width is +1 if the Static includes inline elements.
- Button padding doesn't work when the display is inline