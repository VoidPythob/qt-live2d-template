#pragma once

#include <QOpenGLWidget>

class QLive2DWidget : public QOpenGLWidget
{
    Q_OBJECT
public:
    explicit QLive2DWidget(QWidget *parent = nullptr);
    ~QLive2DWidget() override;

    void resizeGL(int w, int h) override;
};