#include <GL/glut.h>
#include <cmath>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <string>

const int WIDTH = 800;
const int HEIGHT = 600;
const int GAME_DURATION = 60; // 60 seconds = 1 minute

struct Bubble {
    float x, y;
    float radius;
    float speed;
    bool active;
    float burstTime;
};

std::vector<Bubble> bubbles;
int score = 0;
int gameTimeLeft = GAME_DURATION;
bool gameOver = false;

void drawCircle(float x, float y, float radius) {
    glBegin(GL_TRIANGLE_FAN);
    for (int i = 0; i <= 360; i++) {
        float radian = i * 3.14159f / 180;
        glVertex2f(x + cos(radian) * radius, y + sin(radian) * radius);
    }
    glEnd();
}

void drawBubble(const Bubble& bubble) {
    if (bubble.burstTime > 0) {
        // Draw bursting animation
        float burstProgress = (0.3f - bubble.burstTime) / 0.3f;
        glColor4f(1.0f, 1.0f, 1.0f, 1.0f - burstProgress);
        drawCircle(bubble.x, bubble.y, bubble.radius * (1 + burstProgress));
    } else {
        glColor4f(0.0f, 0.5f, 1.0f, 0.5f);  // Semi-transparent blue
        drawCircle(bubble.x, bubble.y, bubble.radius);
        glColor4f(1.0f, 1.0f, 1.0f, 0.7f);  // White highlight
        drawCircle(bubble.x + bubble.radius * 0.3f, bubble.y + bubble.radius * 0.3f, bubble.radius * 0.2f);
    }
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);

    for (const auto& bubble : bubbles) {
        if (bubble.active || bubble.burstTime > 0) {
            drawBubble(bubble);
        }
    }

    // Display score and time
    glColor3f(1.0f, 1.0f, 1.0f);
    glRasterPos2f(10, HEIGHT - 20);
    std::string scoreText = "Score: " + std::to_string(score);
    for (char c : scoreText) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c);
    }

    glRasterPos2f(WIDTH - 150, HEIGHT - 20);
    std::string timeText = "Time left: " + std::to_string(gameTimeLeft) + "s";
    for (char c : timeText) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c);
    }

    if (gameOver) {
        glColor3f(1.0f, 0.0f, 0.0f);
        glRasterPos2f(WIDTH / 2 - 50, HEIGHT / 2);
        std::string gameOverText = "GAME OVER!";
        for (char c : gameOverText) {
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c);
        }
    }

    glutSwapBuffers();
}

void update(int value) {
    if (!gameOver) {
        for (auto& bubble : bubbles) {
            if (bubble.active) {
                bubble.y += bubble.speed;
                if (bubble.y > HEIGHT + bubble.radius) {
                    bubble.active = false;
                }
            } else if (bubble.burstTime > 0) {
                bubble.burstTime -= 0.016f; // Assuming 60 FPS
            }
        }

        // Add new bubbles
        if (rand() % 10 == 0) {
            Bubble newBubble;
            newBubble.x = rand() % WIDTH;
            newBubble.y = -50;
            newBubble.radius = 20 + rand() % 30;
            newBubble.speed = 1 + (rand() % 3);
            newBubble.active = true;
            newBubble.burstTime = 0;
            bubbles.push_back(newBubble);
        }

        glutPostRedisplay();
        glutTimerFunc(16, update, 0);  // 60 FPS
    }
}

void mouse(int button, int state, int x, int y) {
    if (!gameOver && button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
        for (auto& bubble : bubbles) {
            if (bubble.active) {
                float dx = x - bubble.x;
                float dy = (HEIGHT - y) - bubble.y;  // Invert y-coordinate
                float distance = std::sqrt(dx*dx + dy*dy);
                if (distance < bubble.radius) {
                    bubble.active = false;
                    bubble.burstTime = 0.3f; // Set burst animation duration
                    score++;
                    break;
                }
            }
        }
    }
}

void timer(int value) {
    if (!gameOver) {
        gameTimeLeft--;
        if (gameTimeLeft <= 0) {
            gameOver = true;
        }
        glutPostRedisplay();
    }
    if (!gameOver) {
        glutTimerFunc(1000, timer, 0);
    }
}

void init() {
    glClearColor(0.0f, 0.0f, 0.1f, 1.0f);  // Dark blue background
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, WIDTH, 0, HEIGHT);
    glMatrixMode(GL_MODELVIEW);

    // Enable alpha blending for transparency
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    srand(time(nullptr));  // Seed random number generator
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(WIDTH, HEIGHT);
    glutCreateWindow("Bubble Burst - 1 Minute Challenge");

    init();
    glutDisplayFunc(display);
    glutTimerFunc(0, update, 0);
    glutTimerFunc(1000, timer, 0);
    glutMouseFunc(mouse);

    glutMainLoop();
    return 0;
}
