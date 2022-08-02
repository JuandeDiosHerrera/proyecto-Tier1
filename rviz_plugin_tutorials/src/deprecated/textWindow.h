/********************************************************************************
** Form generated from reading UI file 'textwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.2.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef TEXTWINDOW_H
#define TEXTWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextBrowser>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_TextWindow
{
public:
    QWidget *centralWidget;
    QPushButton *pushButton;
    QTextBrowser *textBrowser;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *TextWindow)
    {
        if (TextWindow->objectName().isEmpty())
            TextWindow->setObjectName(QStringLiteral("TextWindow"));
        TextWindow->resize(400, 300);
        centralWidget = new QWidget(TextWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        pushButton = new QPushButton(centralWidget);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setGeometry(QRect(20, 0, 99, 27));
        textBrowser = new QTextBrowser(centralWidget);
        textBrowser->setObjectName(QStringLiteral("textBrowser"));
        textBrowser->setGeometry(QRect(15, 40, 371, 192));
        TextWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(TextWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 400, 25));
        TextWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(TextWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        TextWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(TextWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        TextWindow->setStatusBar(statusBar);

        retranslateUi(TextWindow);

        QMetaObject::connectSlotsByName(TextWindow);
    } // setupUi

    void retranslateUi(QMainWindow *TextWindow)
    {
        TextWindow->setWindowTitle(QApplication::translate("TextWindow", "TextWindow", 0));
        pushButton->setText(QApplication::translate("TextWindow", "PushButton", 0));
    } // retranslateUi

};

namespace Ui {
    class TextWindow: public Ui_TextWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // TEXTWINDOW_H
