#include <stdio.h>
#include "include/raylib.h"
#include "pthread.h"
#include "stdatomic.h"
#include "time.h"
//-------------------------------------------------------------------------------------
#define GLSL_VERSION            330
#define MAX_POSTPRO_SHADERS     12
//-------------------------------------------------------------------------------------
typedef enum{
    FX_GRAYSCALE,
    FX_POSTERIZATION,
    FX_DREAM_VISION=0,
    FX_PIXELIZER,
    FX_CROSS_HATCHING,
    FX_CROSS_STITCHING,
    FX_PREDATOR_VIEW,
    FX_SCANLINES,
    FX_FISHEYE,
    FX_SOBEL,
    FX_BLOOM,
    FX_BLUR,
    //FX_FXAA
} PostProShader;
//-------------------------------------------------------------------------------------
//Main Entry Point
//-------------------------------------------------------------------------------------
int main()
{
    //Initialization
    //---------------------------------------------------------------------------------
    const int WIDTH=800;
    const int HEIGHT=600;
    //--- Window
    InitWindow(WIDTH,HEIGHT,"Terminal");
    //--- Define Camera
    Camera view={{.2f,.4f,.2f},{.0f,.0f,.0f},{.0f,1.0f,.0f},45.0f,0};
    //--- Load Cubicmap (RAM)
    Image L1=LoadImage("textures/CUBIC-MAP/Level_1-MAP.png");
    //--- Convert Image To Texture To Display (VRAM)
    Texture2D L1_cubic=LoadTextureFromImage(L1);
    //--- Create Mesh
    Mesh mesh_L1=GenMeshCubicmap(L1,(Vector3){1.0f,1.0f,1.0f});
    //--- Create Model
    Model L1_model=LoadModelFromMesh(mesh_L1);
    //--- Mapping To Texture Atlas
    Texture2D L1_texture=LoadTexture("textures/CUBIC-TEXTURE/Level_1-TEXTURE.png"); //Load Tex
    L1_model.materials[0].maps[MATERIAL_MAP_DIFFUSE].texture=L1_texture; //Set Diffuse Tex
    //--- Get Map Data For Collision Detection
    Color *mapL1Pixels=LoadImageColors(L1);
    UnloadImage(L1); //Unload Image From RAM
    //----
    Vector3 L1_POS={-16.0f,0.0f,-8.0f}; //Set Model Position
    //----
    Shader shaders[MAX_POSTPRO_SHADERS] = { 0 };
    // NOTE: Defining 0 (NULL) for vertex shader forces usage of internal default vertex shader
    shaders[FX_GRAYSCALE] = LoadShader(0, TextFormat("shaders/glsl%i/grayscale.fs", GLSL_VERSION));
    shaders[FX_POSTERIZATION] = LoadShader(0, TextFormat("shaders/glsl%i/posterization.fs", GLSL_VERSION));
    shaders[FX_DREAM_VISION] = LoadShader(0, TextFormat("shaders/glsl%i/dream_vision.fs", GLSL_VERSION));
    shaders[FX_PIXELIZER] = LoadShader(0, TextFormat("shaders/glsl%i/pixelizer.fs", GLSL_VERSION));
    shaders[FX_CROSS_HATCHING] = LoadShader(0, TextFormat("shaders/glsl%i/cross_hatching.fs", GLSL_VERSION));
    shaders[FX_CROSS_STITCHING] = LoadShader(0, TextFormat("shaders/glsl%i/cross_stitching.fs", GLSL_VERSION));
    shaders[FX_PREDATOR_VIEW] = LoadShader(0, TextFormat("shaders/glsl%i/predator.fs", GLSL_VERSION));
    shaders[FX_SCANLINES] = LoadShader(0, TextFormat("shaders/glsl%i/scanlines.fs", GLSL_VERSION));
    shaders[FX_FISHEYE] = LoadShader(0, TextFormat("shaders/glsl%i/fisheye.fs", GLSL_VERSION));
    shaders[FX_SOBEL] = LoadShader(0, TextFormat("shaders/glsl%i/sobel.fs", GLSL_VERSION));
    shaders[FX_BLOOM] = LoadShader(0, TextFormat("shaders/glsl%i/bloom.fs", GLSL_VERSION));
    shaders[FX_BLUR] = LoadShader(0, TextFormat("shaders/glsl%i/blur.fs", GLSL_VERSION));
    int currentShader = FX_GRAYSCALE;
    // Create a RenderTexture2D to be used for render to texture
    RenderTexture2D target=LoadRenderTexture(WIDTH,HEIGHT);
    //----
    SetCameraMode(view,CAMERA_FIRST_PERSON);
    SetTargetFPS(60);
    //-------------------------------------------------------------------------------------
    //Main Game Loop
    while(!WindowShouldClose()) //Detect Close
    {
        //Update
        //---------------------------------------------------------------------------------
        if (IsKeyPressed(KEY_RIGHT)) currentShader++;
        else if (IsKeyPressed(KEY_LEFT)) currentShader--;
        if (currentShader >= MAX_POSTPRO_SHADERS) currentShader = 0;
        else if (currentShader < 0) currentShader = MAX_POSTPRO_SHADERS - 1;
        //---------------------------------------------------------------------------------
        Vector3 oldCamPos=view.position; //Store Old Position
        UpdateCamera(&view);
        //--- Check Player Collision
        Vector2 playerPOS={view.position.x,view.position.z};
        float playerRadius=0.1f;
        //----
        int playerCellX=(int)(playerPOS.x-L1_POS.x+0.5f);
        int playerCellY=(int)(playerPOS.y-L1_POS.z+0.5f);
        //Out-Of-Limits Security Check
        if(playerCellX<0) playerCellX=0;
        else if(playerCellX>=L1_cubic.width) playerCellX=L1_cubic.width-1;
        if(playerCellY<0) playerCellY=0;
        else if(playerCellY>=L1_cubic.height) playerCellY=L1_cubic.height-1;
        //Check Map Collision
        for(int y=0; y<L1_cubic.height;y++)
        {
            for(int x=0; x<L1_cubic.width;x++)
            {
                if((mapL1Pixels[y*L1_cubic.width+x].r==255) &&
                   (CheckCollisionCircleRec(playerPOS,playerRadius,
                   (Rectangle){L1_POS.x-0.5f+x*1.0f,L1_POS.z-0.5f+y*1.0f,1.0f,1.0f})))
                {
                    //Collision Detected
                    view.position=oldCamPos;
                }
            }
        }
        //---------------------------------------------------------------------------------
        //Draw
        //---------------------------------------------------------------------------------
        BeginTextureMode(target);
            ClearBackground(RAYWHITE);
            BeginMode3D(view);
                DrawModel(L1_model,L1_POS,1.0f,WHITE); //Draw Map
            EndMode3D();
        EndTextureMode();
        BeginDrawing();
            ClearBackground(RAYWHITE);
            // Render generated texture using selected postprocessing shader
            BeginShaderMode(shaders[currentShader]);
                // NOTE: Render texture must be y-flipped due to default OpenGL coordinates (left-bottom)
                DrawTextureRec(target.texture, (Rectangle){ 0, 0, (float)target.texture.width, (float)-target.texture.height }, (Vector2){ 0, 0 }, WHITE);
            EndShaderMode();
             //----
            //DrawTextureEx(L1_cubic,(Vector2){GetScreenWidth()-L1_cubic.width*4.0f-20,20.0f},0.0f,4.0f,WHITE);
            //DrawRectangleLines(GetScreenWidth()-L1_cubic.width*4-20,20,L1_cubic.width*4,L1_cubic.height*4,GREEN);
            //--- Draw Player
            //DrawRectangle(GetScreenWidth()-L1_cubic.width*4-20+playerCellX*4,20+playerCellY*4,4,4,RED);
            DrawFPS(700,15);
        EndDrawing();
    }
    //-------------------------------------------------------------------------------------
    //De-Initialization
    //-------------------------------------------------------------------------------------
    // Unload all postpro shaders
    for (int i = 0; i < MAX_POSTPRO_SHADERS; i++) UnloadShader(shaders[i]);
    UnloadImageColors(mapL1Pixels); //Unload Colour Array
    UnloadTexture(L1_cubic);        //Unload Cubic Texture
    UnloadTexture(L1_texture);      //Unload Map Texture
    UnloadModel(L1_model);          //Unload Model
    CloseWindow();                  //Close Game Window
    //---------------------------------------------------------------------------------
    return 0;
}