#include "LAppDelegate.hpp"
#include <windows.h>

int main()
{
    UINT preConsoleOutputCP = GetConsoleOutputCP();
    SetConsoleOutputCP(65001);

    if (LAppDelegate::GetInstance()->Initialize() == GL_FALSE)
    {
        SetConsoleOutputCP(preConsoleOutputCP);
        return 1;
    }

    LAppDelegate::GetInstance()->Run();

    SetConsoleOutputCP(preConsoleOutputCP);

    return 0;
}